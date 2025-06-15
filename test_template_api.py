from shotstack_sdk import Configuration, ApiClient
from shotstack_sdk.api.edit_api import EditApi

if __name__ == "__main__":
    configuration = Configuration(
        host="https://api.shotstack.io/stage",
        api_key={"x-api-key": "tCXND55PaAJfuunBAFkVAT2r1cH04FkgxxKBec14"}
    )
    api_client = ApiClient(configuration)
    api = EditApi(api_client)
    # Попробуем получить несуществующий рендер (ожидаем ошибку 404, но не 401)
    try:
        result = api.get_render("test")
        print(result)
    except Exception as e:
        print("Ответ от сервера:", e)