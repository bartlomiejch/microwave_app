import redis
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.db import pool
from app.domain import Microwave
from app.services import JsonCacheManager

SECRET_KEY = "secret"
ALGORITHM = "HS256"
MICROWAVE_CACHE_KEY = "app"

app = FastAPI(title="Microwave")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token JWT")


def get_redis():
    return redis.Redis(connection_pool=pool)


def get_microwave():
    return Microwave()


def get_json_cache_manager():
    return JsonCacheManager()


@app.get("/current_state")
def current_state(jcm=Depends(get_json_cache_manager),
                  microwave=Depends(get_microwave),
                  cache=Depends(get_redis)):
    microwave.load(jcm.get(cache, MICROWAVE_CACHE_KEY))
    return {"message": microwave.get_state()}


@app.get("/power_up")
def power_up(jcm=Depends(get_json_cache_manager),
             microwave=Depends(get_microwave),
             cache=Depends(get_redis)):
    microwave.load(jcm.get(cache, MICROWAVE_CACHE_KEY))
    microwave.power_up()
    jcm.set(cache, MICROWAVE_CACHE_KEY, microwave.get_state())
    return {"message": microwave.get_message()}


@app.get("/power_down")
def power_down(jcm=Depends(get_json_cache_manager),
               microwave=Depends(get_microwave),
               cache=Depends(get_redis)):
    microwave.load(jcm.get(cache, MICROWAVE_CACHE_KEY))
    microwave.power_down()
    jcm.set(cache, MICROWAVE_CACHE_KEY, microwave.get_state())
    return {"message": microwave.message}


@app.get("/counter_up")
def counter_up(jcm=Depends(get_json_cache_manager),
               microwave=Depends(get_microwave),
               cache=Depends(get_redis)):
    microwave.load(jcm.get(cache, MICROWAVE_CACHE_KEY))
    microwave.counter_up()
    jcm.set(cache, MICROWAVE_CACHE_KEY, microwave.get_state())
    return {"message": microwave.get_message()}


@app.get("/counter_down")
def counter_down(
        jcm=Depends(get_json_cache_manager),
        microwave=Depends(get_microwave),
        cache=Depends(get_redis)):
    microwave.load(jcm.get(cache, MICROWAVE_CACHE_KEY))
    microwave.counter_down()
    jcm.set(cache, MICROWAVE_CACHE_KEY, microwave.get_state())
    return {"Message": microwave.get_message()}


@app.get("/cancel")
def cancel(
    jcm=Depends(get_json_cache_manager),
    microwave=Depends(get_microwave),
    payload: dict = Depends(decode_jwt_token),
    cache=Depends(get_redis),
):
    if "role" in payload and payload["role"] == "manager":
        microwave.load(jcm.get(cache, MICROWAVE_CACHE_KEY))
        microwave.cancel()
        jcm.set(cache, MICROWAVE_CACHE_KEY, microwave.get_state())
        return {"message": f"{microwave.get_message()}"}
    else:
        raise HTTPException(
            status_code=403, detail="User is not authorized to"
                                    " cancel the microwave."
        )
