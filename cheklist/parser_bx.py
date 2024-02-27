from fast_bitrix24 import BitrixAsync
import asyncio
from .parser_contact import bitrix_1c_contact
async def bitrix_1c_s(deal_id):
    webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
    b = BitrixAsync(webhook)
    method = 'crm.deal.get'
    params = {"id": deal_id}


    # Выполняем запрос
    result = await b.call(method, params, raw=True)

    # Извлекаем нужные данные
    deal_data = result.get('result', {})
    report_executor_model_adress = deal_data.get('UF_CRM_1674993837284',)
    report_executor_model_lis_schet = deal_data.get('UF_CRM_1673255771',)
    report_executor_model_application_info = deal_data.get('UF_CRM_1673258743852',)


    contact_id = deal_data.get('CONTACT_ID', None)
    contact_data = {}
    if contact_id:
        contact_data = await bitrix_1c_contact(contact_id)  # Используйте асинхронный вызов


    extracted_data = {
        "адрес": report_executor_model_adress,
        "Лицовой_счет": report_executor_model_lis_schet,
        "Описание_заявки": report_executor_model_application_info,
    }
    extracted_data.update(contact_data)
    return extracted_data

def main():
    deal_id = 90779
    # Используем новый цикл событий для запуска асинхронной функции
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(bitrix_1c_s(deal_id))
    print(data)

# Проверяем, является ли скрипт точкой входа в программу
if __name__ == '__main__':
    main()
