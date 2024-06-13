from fastapi import Header, HTTPException

def validate_api_key(x_api_key: str = Header(...)):
    if x_api_key != "ZtVdh8XQ2U8pWI2gmZ7f796Vh8GllXoN7mr0djNf":
        raise HTTPException(status_code=403, detail="x-api-key header missing or invalid")
