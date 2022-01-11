import json
import aiofiles


class HypyObject:
    """A base object for API Data"""

    _raw: dict

    async def save_json(self, filename) -> None:
        """Save raw API data to disk

        :param filename: The name of the file to save to
        """
        async with aiofiles.open(filename, mode="w+") as f:
            await f.write(json.dumps(self._raw, indent=4))
