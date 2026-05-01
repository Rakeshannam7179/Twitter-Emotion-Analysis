import traceback
try:
    from fastapi import FastAPI
    import uvicorn
    uvicorn.run("main:app", port=8000)
except Exception as e:
    with open("err.txt", "w") as f:
        f.write(traceback.format_exc())
