from typing import Optional

import aiohttp


async def download_file(file_url: str, file_path: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as resp:
                if resp.status != 200:
                    print(f"Failed to download file. Status: {resp.status}")
                    return None

                with open(file_path, "wb") as f:
                    f.write(await resp.read())
        return file_path
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None
