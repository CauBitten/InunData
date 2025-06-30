from fastapi import FastAPI # type: ignore

app = FastAPI()


@app.get('monthly_city_rainfall/{month_year}')
async def monthly_city_rainfall(month_year: str):
    ''''''
