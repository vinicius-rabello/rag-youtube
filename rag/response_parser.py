from rag.helpers import convert_seconds_to_time

def parse_response(response, relevant_chunks):
    formatted_response = response
    formatted_response = {"response": response, "timestamps": []}
    for chunk in relevant_chunks[:3]:
        start = convert_seconds_to_time(chunk.metadata["start"])
        end = convert_seconds_to_time(chunk.metadata["end"])
        formatted_response["timestamps"].append(f"{start} - {end}")
    return formatted_response