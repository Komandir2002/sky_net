from fast_bitrix24 import BitrixAsync
import asyncio

async def bitrix_1c_contact(deal_id):
    webhook = "https://bitrix24.snt.kg/rest/87/e8rzilwpu7u998y7/"
    b = BitrixAsync(webhook)
    method = 'crm.contact.get'
    params = {"id": deal_id}

    # Выполняем запрос
    result = await b.call(method, params, raw=True)

    # Извлекаем нужные данные
    deal_data = result.get('result', {})
    report_executor_model_phone = deal_data.get('PHONE', [{}])[0].get('VALUE', 'Нет телефона')
    report_executor_model_name = deal_data.get('NAME',)
    report_executor_model_last_name = deal_data.get('LAST_NAME',)


    extracted_data = {
        "PHONE": report_executor_model_phone,
        "LAST_NAME": report_executor_model_name,
        "NAME": report_executor_model_last_name,
    }
    return extracted_data