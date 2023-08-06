import math

import pytest

from usim import time, until, eternity, instant, delay, interval, IntervalExceeded

from ..utility import via_usim, assertion_mode


async def aenumerate(aiterable, start=0):
    count = start
    async for item in aiterable:
        yield count, item
        count += 1


class TestTime:
    @via_usim
    async def test_representable(self):
        for case in (time, time < 1, time >= 1, time + 1, eternity, instant):
            str(case), repr(case)

    @via_usim
    async def test_misuse(self):
        with pytest.raises(TypeError):
            await time
        with pytest.raises(TypeError):
            await (time <= 100)
        with pytest.raises(TypeError):
            ~(time + 3)
        with pytest.raises(TypeError):
            (time + 3) & (time == 3)
        with pytest.raises(TypeError):
            (time + 3) | (time == 3)

    @assertion_mode
    @via_usim
    async def test_debug_misuse(self):
        with pytest.raises(AssertionError):
            await (time + -1)

    @via_usim
    async def test_delay(self):
        start, delay = time.now, 20
        for seq in range(5):
            assert start + (delay * seq) == time.now
            await (time + delay)
        assert start + (delay * 5) == time.now
        # allow for 0 delay
        await (time + 0)
        assert start + (delay * 5) == time.now

    @via_usim
    async def test_moment(self):
        start, delay = time.now, 20
        for seq in range(5):
            await (time == start + seq * delay)
            assert start + (delay * seq) == time.now
        assert start + (delay * 4) == time.now

    @via_usim
    async def test_previous_moment(self):
        start, delay = time.now, 20
        async with until(time == start + delay):
            await (time == start - 5)  # await moment in the past
            assert False, "Moment in the past should never pass"
        assert start + delay == time.now

    @via_usim
    async def test_after(self):
        start, delay = time.now, 20
        for seq in range(5):
            await (time >= start + seq * delay)
            assert start + (delay * seq) == time.now
        assert start + (delay * 4) == time.now

    @via_usim
    async def test_previous_after(self):
        start, delay = time.now, 20
        async with until(time == start + delay):
            await (time >= start - 5)  # await moment in the past
            assert True, "After in the past should always pass"
        assert start == time.now

    @via_usim
    async def test_before(self):
        start, delay = time.now, 20
        for seq in range(1, 5):
            await (time < start + seq * delay)
            assert start == time.now
        assert start == time.now

    @via_usim
    async def test_previous_before(self):
        start, delay = time.now, 20
        async with until(time == start + delay):
            await (time < start - 5)  # await moment in the past
            assert False, "Before in the past should never pass"
        assert start + delay == time.now

    @via_usim
    async def test_infinity(self):
        await (time == math.inf)
        assert math.inf == time.now

    @via_usim
    async def test_infinity_ge(self):
        await (time >= math.inf)
        assert math.inf == time.now


class TestTimeCondition:
    @via_usim
    async def test_after(self):
        start = time.now
        assert (time >= time.now)
        assert not (time >= time.now + 20)
        assert not ~(time >= time.now)
        assert ~(time >= time.now + 20)
        await (time >= time.now)
        await (time >= time.now + 20)
        assert time.now == start + 20

    @via_usim
    async def test_before(self):
        start = time.now
        assert not (time < time.now)
        assert (time < time.now + 20)
        assert ~(time < time.now)
        assert not ~(time < time.now + 20)
        await (time < time.now + 20)
        async with until(time + 20):
            await (time < time.now)
        assert time.now == start + 20

    @via_usim
    async def test_moment(self):
        start = time.now
        assert (time == start)
        assert not (time == start + 20)
        await (time == start + 20)
        assert not (time == start)
        assert (time == start + 20)
        assert time.now == start + 20

    @via_usim
    async def test_extremes(self):
        start = time.now
        assert instant
        assert not eternity
        assert not ~instant
        assert ~eternity
        await (time == start + 20)
        assert instant
        assert not eternity
        assert not ~instant
        assert ~eternity
        assert time.now == start + 20


class TestTimeIteration:
    @via_usim
    async def test_misuse(self):
        with pytest.raises(ValueError):
            async for _ in delay(-1):
                pass
        with pytest.raises(ValueError):
            async for _ in interval(-1):
                pass

    @via_usim
    async def test_delay(self):
        start, iteration = time.now, 0
        async for now in delay(20):
            iteration += 1
            await (time + 5)
            assert time.now - now == 5
            assert time.now == start + iteration * 25
            if iteration == 5:
                break

    @via_usim
    async def test_delay_exact(self):
        async for idx, _ in aenumerate(delay(0)):
            assert time.now == 0
            if idx > 5:
                break
        async for idx, _ in aenumerate(delay(0)):
            assert time.now == idx * 5
            await (time + 5)
            if idx > 5:
                break

    @via_usim
    async def test_interval(self):
        start, iteration = time.now, 1
        async for now in interval(20):
            await (time + 5)
            assert time.now - now == 5
            assert time.now == start + iteration * 20 + 5
            if iteration == 5:
                break
            iteration += 1

    @via_usim
    async def test_interval_exceeded(self):
        """It is an error to exceed an interval"""
        try:
            async for _ in interval(20):
                await (time + 40)
        except IntervalExceeded:
            assert True
        else:
            assert False

    @via_usim
    async def test_interval_exact(self):
        """It is not an error to exactly match an interval"""
        try:
            async for idx, _ in aenumerate(interval(20)):
                await (time + 20)
                if idx == 5:
                    break
        except IntervalExceeded:
            assert False
        else:
            assert True
