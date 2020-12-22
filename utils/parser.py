
class Parser:
    '''
    Clase con metodos para parsing de tweets 
    '''
    @staticmethod
    def error_handler(key,data):
        try:
            value = data[key]
        except:
            value = None
        return value

    @staticmethod
    def parse_entity(entity,data):
        try:
            entity_content = data["entities"][entity]

            if entity == "user_mentions":
                result = [i["screen_name"] for i in entity_content]

            elif entity == "hashtags":
                result = [i["text"] for i in entity_content]
        except:
            result = None
        return result
    


def parse_json(data):

    
    parsed_data = {}
    parsed_data["created_at"] = Parser.error_handler("created_at",data)
    parsed_data["id"] = Parser.error_handler("id_str",data)
    parsed_data["user_id"] = Parser.error_handler("id_str",data["user"])
    parsed_data["user_name"] = Parser.error_handler("name",data["user"])
    parsed_data["user_screen_name"] = Parser.error_handler("screen_name",data["user"])
    parsed_data["text"] = Parser.error_handler("text",data)
    parsed_data["lang"] = Parser.error_handler("lang",data)
    parsed_data["hashtags"] = Parser.parse_entity("hashtags",data)
    parsed_data["user_mentions"] = Parser.parse_entity("user_mentions",data)
    parsed_data["source"] = Parser.error_handler("source",data)
    parsed_data["coords"] = Parser.error_handler("coordinates",data["coordinates"])
    parsed_data["coords_type"] = Parser.error_handler("type",data["coordinates"])
    parsed_data["is_quote"] = Parser.error_handler("is_quote_status",data)
    parsed_data["is_retweet"] = Parser.error_handler("retweeted",data)
    parsed_data["is_reply"] = Parser.error_handler("in_reply_to_user_id_str",data)
    parsed_data["is_reply"] = Parser.error_handler("in_reply_to_user_id_str",data)
    parsed_data["truncated"] = data.get('truncated')

    return parsed_data
