from fastapi import APIRouter, HTTPException, Depends
from typing import List
import httpx
from .dependencies import validate_api_key
from .models import Broth, Protein, OrderRequest, OrderResponse
from data.broths import broths_db
from data.proteins import proteins_db

router = APIRouter()


@router.get("/broths", response_model=List[Broth])
async def list_broths(x_api_key: str = Depends(validate_api_key)):
    return broths_db


@router.get("/proteins", response_model=List[Protein])
async def list_proteins(x_api_key: str = Depends(validate_api_key)):
    return proteins_db


@router.post("/orders", response_model=OrderResponse)
async def place_order(order_request: OrderRequest, x_api_key: str = Depends(validate_api_key)):
    if not order_request.brothId or not order_request.proteinId:
        raise HTTPException(status_code=400, detail="both brothId and proteinId are required")

    broth = next((b for b in broths_db if b["id"] == order_request.brothId), None)
    protein = next((p for p in proteins_db if p["id"] == order_request.proteinId), None)

    if not broth or not protein:
        raise HTTPException(status_code=400, detail="Invalid brothId or proteinId")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.tech.redventures.com.br/orders/generate-id",
            headers={"x-api-key": "ZtVdh8XQ2U8pWI2gmZ7f796Vh8GllXoN7mr0djNf"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="could not place order")

        order_id = response.json().get("orderId")

    order_description = f"{broth['name']} and {protein['name']} Ramen"
    order_image = "https://tech.redventures.com.br/icons/ramen/ramenChasu.png"

    return {
        "id": order_id,
        "description": order_description,
        "image": order_image,
    }
