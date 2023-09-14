import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Union

app = FastAPI()

# Definir un diccionario vacío para almacenar la información de los usuarios
usuarios = {}

# Definir el modelo Pydantic para la creación de usuarios
class UsuarioCreate(BaseModel):
    user_name: str
    user_id: int
    user_email: str
    age: Union[int, None] = None
    recommendations: List[str]
    ZIP: Union[str, None] = None

# Endpoint para crear un usuario
@app.post("/crear_usuario/")
def crear_usuario(usuario: UsuarioCreate):
    user_id = usuario.user_id

    if user_id in usuarios:
        raise HTTPException(status_code=400, detail=f"El ID {user_id} ya existe")

    usuarios[user_id] = usuario.dict()
    return {"id": user_id, "message": "Usuario creado exitosamente"}

# Endpoint para actualizar la información de un usuario
@app.put("/actualizar_usuario/{user_id}")
def actualizar_usuario(user_id: int, usuario: UsuarioCreate):
    if user_id not in usuarios:
        raise HTTPException(status_code=404, detail=f"El ID {user_id} no existe")

    usuarios[user_id].update(usuario.dict(exclude_unset=True))
    return {"message": f"Información del usuario {user_id} actualizada"}

# Endpoint para obtener la información de un usuario
@app.get("/obtener_usuario/{user_id}")
def obtener_usuario(user_id: int):
    if user_id not in usuarios:
        raise HTTPException(status_code=404, detail=f"El ID {user_id} no existe")

    return usuarios[user_id]

# Endpoint para eliminar la información de un usuario
@app.delete("/eliminar_usuario/{user_id}")
def eliminar_usuario(user_id: int):
    if user_id not in usuarios:
        raise HTTPException(status_code=404, detail=f"El ID {user_id} no existe")

    del usuarios[user_id]
    return {"message": f"Usuario {user_id} eliminado"}

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5021, log_level="info", reload=False)