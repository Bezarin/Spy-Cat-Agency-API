import httpx

CATAPI_URL = "https://api.thecatapi.com/v1/breeds"


async def is_valid_breed(breed: str) -> bool:
    breed = breed.strip().lower()
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(CATAPI_URL)
        response.raise_for_status()
        names = {item["name"].strip().lower() for item in response.json()}
    return breed in names
