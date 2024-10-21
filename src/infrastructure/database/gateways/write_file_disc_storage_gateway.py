from src.application.interfaces.gateways import IWriteFileStorageGateway
from pathlib import Path


class WriteFileDiscStorageGateway(IWriteFileStorageGateway):
    async def safe_file_in_storage(self, save_directory, file):
        SAVE_DIRECTORY = Path("/usr/src/app/media" + save_directory)
        SAVE_DIRECTORY.mkdir(parents=True, exist_ok=True)
        file_location = SAVE_DIRECTORY / file.filename
        with open(file_location, "wb") as f:
            f.write(await file.read())
        print('---->file data<-----------')
        print(file.filename)
        print(file_location)
        print(f"file '{file.filename}' saved at '{file_location}'")
        print('---------------------------')
        return {"info": f"file '{file.filename}' saved at '{file_location}'"}