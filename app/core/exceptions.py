from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = []

    for error in exc.errors():
        if error["type"] == "json_invalid":
            errors.append({
                "property": "body",
                "message": "El cuerpo de la petición no contiene un JSON válido",
            })
            continue

        field = ".".join(
            str(value) for value in error["loc"][1:]
        )

        if error["type"] == "missing":
            message = "El campo es obligatorio"
        else:
            message = error["msg"].removeprefix("Value error, ")

        errors.append({
            "property": field,
            "message": message,
        })

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"errors": errors},
    )
