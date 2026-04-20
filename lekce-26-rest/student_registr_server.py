from fastapi import FastAPI, HTTPException

from student_registr_impl import StudentRegistrImpl
from student_registr_kontrakt import Student, StudentRegistr

# --- FastAPI RPC server ---

app = FastAPI(title="StudentRegistr RPC")
registr = StudentRegistrImpl()


@app.get("/pridej_studenta")
def pridej_studenta(student_id: int, jmeno: str, vek: int) -> dict:
    try:
        registr.pridej_studenta(student_id, jmeno, vek)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return {"status": "ok"}


@app.get("/odeber_studenta")
def odeber_studenta(student_id: int) -> dict:
    try:
        registr.odeber_studenta(student_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"status": "ok"}


@app.get("/najdi_studenta")
def najdi_studenta(student_id: int) -> Student | None:
    return registr.najdi_studenta(student_id)


@app.get("/pocet_studentu")
def pocet_studentu() -> dict:
    return {"pocet": registr.pocet_studentu()}


@app.get("/vsichni_studenti")
def vsichni_studenti() -> list[Student]:
    return registr.vsichni_studenti()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)