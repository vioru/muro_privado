from flask_app.config.mysqlconnection import connectToMySQL

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.text = data['text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']

        #2 propiedades extra que vamos a obtener gracias al LEFT JOIN
        self.sender_name = data['sender_name']
        self.receiver_name = data['receiver_name']

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO messages (text, sender_id, receiver_id) VALUES (%(text)s, %(sender_id)s, %(receiver_id)s)"
        result = connectToMySQL('wall').query_db(query, formulario)
        return result

    @classmethod 
    def get_user_messages(cls, formulario):
        query = "SELECT messages.*, receivers.first_name as receiver_name, senders.first_name as sender_name FROM messages LEFT JOIN users as receivers ON receivers.id = receiver_id LEFT JOIN users as senders ON senders.id = sender_id WHERE receiver_id = %(id)s;"
        results = connectToMySQL('wall').query_db(query, formulario)
        messages =[]
        for message in results:
            messages.append(cls(message))
        
        return messages
    
    @classmethod 
    def get_messages_id(cls, formulario):
        query = "SELECT messages.*, receivers.first_name as receiver_name, senders.first_name as sender_name FROM messages LEFT JOIN users as receivers ON receivers.id = receiver_id LEFT JOIN users as senders ON senders.id = sender_id WHERE messages.id = %(id)s;"
        results = connectToMySQL('wall').query_db(query, formulario)
        return cls(results[0])       

    @classmethod
    def eliminate(cls,formulario):
        query= "DELETE FROM messages WHERE id = %(id)s"
        result = connectToMySQL('wall').query_db(query,formulario)
        return result



