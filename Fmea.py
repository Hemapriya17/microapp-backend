from flask import  jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import pandas as pd
import sys
from pymongo import MongoClient
from bson import ObjectId


MOLGODBURL = "mongodb+srv://mugil:mugil@cluster0.ewo6rku.mongodb.net/?retryWrites=true&w=majority"
print(MOLGODBURL,file=sys.stderr)
client = MongoClient(MOLGODBURL)
db = client['MicroApp']  
collection = db['Fmea_collection']




def generate_fmea(request):
    load_dotenv()   
    OPENAPIKEY = os.getenv("OPEN_AI_KEY")
    try:
        client = OpenAI(api_key=OPENAPIKEY)
        data = request.get_json()
        fmea_name = data["fmeaName"]
        # prompt = f'generate full design FMEA for {fmea_name} in a table format and add at least 3 failure modes for each of the item/function?. Only return the generated FMEA table and don"t return any unwanted texts.'
        prompt = f'Generate full design FMEA for {fmea_name} in a table format with the following headers id, Item/Component, Function, Requirement, Potential Failure mode, Potential Effects of failure, Severity, Classification, Potential Cause of the failure, Occurrences, Current Controls(Prevention), Current Controls (Detection), Detection, RPN, Recommended Action, Responsibility & target Completion date, Action Taken & Effective Date, Severity, Occurrence, Detection and RPN. Derive 3 levels of functions and 3 levels of requirements for each component/item. Then add at least 3 failure modes for each of the requirements?. Only return the generated FMEA table and don"t return any unwanted texts.'

        messages = [{"role": "user", "content": prompt}]
        start_time = time.time()
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview", messages=messages, temperature=0
        )
        end_time = time.time()
        time_lapsed = end_time - start_time
        text = completion.choices[0].message.content

        table_content = text.split("\n")[2:-2]
        table_content = [row.split("|")[1:-1] for row in table_content]

        header = [h.strip() for h in text.split("\n")[0].split("|")[1:-1]]


        df = pd.DataFrame(table_content, columns=header)

        csv_data = df.to_dict(orient='records')

        print(csv_data,file=sys.stderr)
        return jsonify({"csv_data": csv_data, "timeElapsed": round(time_lapsed, 2)})

    except Exception as e:
        print(str(e), file=sys.stderr)
        return jsonify({"error": str(e)}), 500




def store_fmea(request):
     data = request.get_json()
     print(data,file=sys.stderr)  
     collection.insert_one(data)
     return jsonify({"response": "got it"})



def getall_fmea(request):
    results = collection.find({ 'name': 'mugilanmourougayen@gmail.com' }, { '_id': 1, 'prompt': 1 ,'service':1})
    result_list = [{'_id': str(result['_id']), 'prompt': result['prompt'],'service':result['service']} for result in results]
    return jsonify(result_list)



def getone_fmea(request):
    id=request.get_json()
    print(id,file=sys.stderr)
    results = collection.find_one({ '_id': ObjectId(id['id'])})
    results['_id'] = str(results['_id'])
    print(results,file=sys.stderr)
    return jsonify(results)