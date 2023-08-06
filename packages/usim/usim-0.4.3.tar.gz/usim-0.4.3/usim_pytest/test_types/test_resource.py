import pytest
import math
from typing import Type

from usim import Scope, time, until
from usim import Resources, Capacities, ResourcesUnavailable
from usim.typing import ResourceLevels
from usim._basics.resource import BaseResources

from ..utility import via_usim, assertion_mode


class TestResourceLevels:
    def test_misuse(self):
        with pytest.raises(TypeError):
            ResourceLevels()
        with pytest.raises(TypeError):
            ResourceLevels(a=3, b=4)

    def test_comparison(self):
        resource_type = Resources(a=3, b=3).resource_type
        assert resource_type(a=5, b=10) == resource_type(b=10, a=5)
        assert resource_type(a=5, b=10) != resource_type(a=6, b=10)
        assert resource_type(a=5, b=10) < resource_type(a=6, b=11)
        assert not resource_type(a=5, b=10) < resource_type(a=6, b=10)
        assert resource_type(a=5, b=10) <= resource_type(a=6, b=10)
        assert resource_type(a=6, b=11) > resource_type(a=5, b=10)
        assert not resource_type(a=6, b=10) > resource_type(a=5, b=10)
        assert resource_type(a=6, b=10) >= resource_type(a=5, b=10)
        assert resource_type(a=5, b=10) + resource_type(a=10, b=5) ==\
            resource_type(b=15, a=15)
        assert resource_type(a=25, b=20) - resource_type(a=10, b=5) ==\
            resource_type(b=15, a=15)


class BaseResourceCase:
    resource_type = None  # type: Type[BaseResources]

    @via_usim
    async def test_misuse(self):
        with pytest.raises(TypeError):
            self.resource_type()

    @assertion_mode
    @via_usim
    async def test_debug_misuse(self):
        with pytest.raises(AssertionError):
            self.resource_type(a=10, b=-10)
        resources = self.resource_type(a=10, b=10)
        with pytest.raises(AssertionError):
            async with resources.borrow(a=-1, b=-1):
                pass
        with pytest.raises(AssertionError):
            async with resources.borrow(a=-1):
                pass
        with pytest.raises(AssertionError):
            async with resources.borrow(b=-1):
                pass

    @via_usim
    async def test_borrow(self):
        resources = self.resource_type(a=10, b=10)
        async with resources.borrow(a=5, b=5):
            assert True
        async with resources.borrow(a=5):
            assert True
        async with resources.borrow(b=5):
            assert True
        async with resources.borrow(a=7, b=7):
            assert True
        async with resources.borrow(a=10, b=10):
            assert True

    @via_usim
    async def test_claim(self):
        resources = self.resource_type(a=10, b=10)
        # test that we can claim below capacity
        async with resources.claim(a=5, b=5):
            assert True
        async with resources.claim(a=5):
            assert True
        async with resources.claim(b=5):
            assert True
        async with resources.claim(a=7, b=7):
            assert True
        async with resources.claim(a=10, b=10):
            assert True
        # test that we cannot claim beyond capacity
        async with resources.claim(a=5, b=5):
            with pytest.raises(ResourcesUnavailable):
                async with resources.claim(a=10, b=10):
                    assert False
            with pytest.raises(ResourcesUnavailable):
                async with resources.claim(a=10):
                    assert False
            with pytest.raises(ResourcesUnavailable):
                async with resources.claim(b=10):
                    assert False
            with pytest.raises(ResourcesUnavailable):
                async with resources.claim(a=10, b=5):
                    assert False
            with pytest.raises(ResourcesUnavailable):
                async with resources.claim(a=5, b=10):
                    assert False

    @via_usim
    async def test_nested_borrow(self):
        resources = self.resource_type(a=10, b=10)
        async with resources.borrow(a=5, b=5):
            async with resources.borrow(a=5, b=5):
                assert True
            async with resources.borrow(a=5):
                assert True
            async with resources.borrow(b=5):
                assert True
        async with resources.borrow(a=7, b=7):
            async with resources.borrow(a=3, b=3):
                assert True
        async with resources.borrow(a=10, b=10):
            assert True

    @via_usim
    async def test_recursive_borrow(self):
        resources = self.resource_type(a=10, b=10)
        async with resources.borrow(a=5, b=5) as sub_resource:
            async with sub_resource.borrow(a=5, b=5):
                assert True
            async with sub_resource.borrow(a=5):
                assert True
            async with sub_resource.borrow(b=5):
                assert True
        async with resources.borrow(a=7, b=7) as sub_resource:
            async with sub_resource.borrow(a=3, b=3):
                assert True
        async with resources.borrow(a=10, b=10):
            assert True

    @via_usim
    async def test_borrow_atomicity(self):
        """Test that a borrow will succeed at once"""
        async def borrow_nowait(duration, **amounts):
            """Borrow resources only if possible"""
            # if `borrow` is not atomic, this check will run *before*
            # an eventual owner has actually acquired the resources.
            if resources.resource_type(**amounts) > resources.levels:
                return
            async with resources.borrow(**amounts):
                await (time + duration)

        resources = self.resource_type(a=1, b=1)
        async with Scope() as scope:
            scope.do(borrow_nowait(10, a=1, b=1))
            scope.do(borrow_nowait(10, a=1, b=1))
        assert time == 10

    @via_usim
    async def test_congested(self):
        resources = self.resource_type(a=10, b=10)

        async def borrow(duration, **amounts):
            async with resources.borrow(**amounts):
                await (time + duration)

        assert time == 0
        async with Scope() as scope:
            scope.do(borrow(10, a=6, b=4))
            scope.do(borrow(10, a=6, b=4))  # not compatible with 1)
            scope.do(borrow(10, a=4, b=6))  # compatible with 1) and 2)
        assert time == 20

    @via_usim
    async def test_release(self):
        """Release resources from cancelled tasks"""
        resources = self.resource_type(a=10, b=10)

        async def block(**amounts):
            async with resources.borrow(**amounts):
                await (time + math.inf)

        assert time == 0
        async with Scope() as scope:
            task_a = scope.do(block(a=4, b=4))
            task_b = scope.do(block(a=4, b=4))
            await (time + 10)
            task_a.cancel()
            task_b.__close__()
        async with resources.borrow(a=10, b=10):
            assert time == 10

    @via_usim
    async def test_compare(self):
        resources = self.resource_type(a=10, b=10)

        async def borrow_shortly(resource: BaseResources, **amounts):
            async with resource.borrow(**amounts):
                pass

        async with Scope() as scope:
            await (resources == {'a': 10, 'b': 10})
            scope.do(borrow_shortly(resources, a=5, b=5), after=10)
            await (resources == resources.resource_type(a=5, b=5))
            assert time.now == 10
        assert time.now == 10
        async with Scope() as scope:
            await (resources > {'a': 9, 'b': 9})
            scope.do(borrow_shortly(resources, a=5, b=5), after=10)
            await (resources > resources.resource_type(a=5, b=5))
            assert time.now == 10
        assert time.now == 20
        async with Scope() as scope:
            await (resources >= {'a': 10, 'b': 10})
            scope.do(borrow_shortly(resources, a=5, b=5), after=10)
            await (resources >= resources.resource_type(a=5, b=5))
            assert time.now == 20
        assert time.now == 30
        async with Scope() as scope:
            await (resources <= {'a': 10, 'b': 10})
            scope.do(borrow_shortly(resources, a=5, b=5), after=10)
            await (resources <= resources.resource_type(a=5, b=5))
            assert time.now == 40
        assert time.now == 40
        async with Scope() as scope:
            await (resources < {'a': 11, 'b': 11})
            scope.do(borrow_shortly(resources, a=5, b=5), after=10)
            await (resources < resources.resource_type(a=6, b=6))
            assert time.now == 50
        assert time.now == 50
        async with Scope() as scope:
            await (resources != {'a': 5, 'b': 5})
            scope.do(borrow_shortly(resources, a=5, b=5), after=10)
            await (resources != resources.resource_type(a=10, b=10))
            assert time.now == 60
        assert time.now == 60


class TestCapacity(BaseResourceCase):
    resource_type = Capacities

    @via_usim
    async def test_limits(self):
        resources = Capacities(a=10, b=10)
        assert resources.limits == resources.resource_type(a=10, b=10)
        assert resources.limits == resources.levels
        async with resources.borrow(a=5, b=5):
            assert resources.limits > resources.levels
            assert resources.limits == resources.resource_type(a=10, b=10)

    @assertion_mode
    @via_usim
    async def test_borrow_exceed(self):
        resources = Capacities(a=10, b=10)
        with pytest.raises(AssertionError):
            async with resources.borrow(a=11, b=11):
                pass
        with pytest.raises(AssertionError):
            async with resources.borrow(a=11, b=10):
                pass
        with pytest.raises(AssertionError):
            async with resources.borrow(a=10, b=11):
                pass
        with pytest.raises(AssertionError):
            async with resources.borrow(a=11):
                pass
        with pytest.raises(AssertionError):
            async with resources.borrow(b=11):
                pass
        # check that borrowing does not always raise
        async with resources.borrow(b=10, a=10):
            assert True


class TestResources(BaseResourceCase):
    resource_type = Resources

    @via_usim
    async def test_increase(self):
        resources = Resources(a=10, b=10)
        async with resources.borrow(a=10, b=10):
            await resources.increase(a=10, b=10)
            async with resources.borrow(a=10, b=10):
                await resources.increase(a=20, b=20)
                async with resources.borrow(a=20, b=20):
                    assert True
        async with resources.borrow(a=40, b=40):
            assert True

    @assertion_mode
    @via_usim
    async def test_increase_misuse(self):
        resources = Resources(a=10, b=10)
        with pytest.raises(AssertionError):
            await resources.increase(a=-1, b=-1)
        with pytest.raises(AssertionError):
            await resources.increase(a=-1)
        with pytest.raises(AssertionError):
            await resources.increase(b=-1)

    @via_usim
    async def test_decrease(self):
        resources = Resources(a=40, b=40)
        async with resources.borrow(a=20, b=20):
            await resources.decrease(a=10, b=10)
            async with until(time == 10):
                async with resources.borrow(a=20, b=20):
                    assert False
            assert time == 10
        async with resources.borrow(a=30, b=30):
            assert True
        async with until(time == 20):
            async with resources.borrow(a=40, b=40):
                assert False
        assert time == 20

    @assertion_mode
    @via_usim
    async def test_decrease_misuse(self):
        resources = Resources(a=10, b=10)
        with pytest.raises(AssertionError):
            await resources.decrease(a=-1, b=-1)
        with pytest.raises(AssertionError):
            await resources.decrease(a=-1)
        with pytest.raises(AssertionError):
            await resources.decrease(b=-1)
        # decrease below zero
        with pytest.raises(AssertionError):
            await resources.decrease(a=20, b=20)

    @via_usim
    async def test_set(self):
        resources = Resources(a=10, b=10)
        await resources.set(a=20, b=20)
        async with resources.borrow(a=20, b=20):
            assert True
        await resources.set(a=30)
        async with resources.borrow(a=30, b=20):
            assert True
        await resources.set(b=30)
        async with resources.borrow(a=30, b=30):
            assert True

    @assertion_mode
    @via_usim
    async def test_set_misuse(self):
        resources = Resources(a=10, b=10)
        with pytest.raises(AssertionError):
            await resources.set(a=-1, b=-1)
        with pytest.raises(AssertionError):
            await resources.set(a=-1)
        with pytest.raises(AssertionError):
            await resources.set(b=-1)
