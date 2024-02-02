from openai import OpenAI


class Chat:
    def __init__(self):
        self.client = OpenAI()
        self.model = "gpt-3.5-turbo"

    def set_initial_message(self, user_name):
        self.initial_message = [
            {"role": "system",
             "content": f"Du bist ein Psychologe, der Menschen wie {user_name} in stressigen Situationen hilft "
                        f"Wege zu finden, um einen besseren Ausgleich zu haben. "
                        f"Du stellst gezielt 3 Fragen zum aktuellen mentalen Wohlbefinden, "
                        f"dem sozialen Umfeld und der Arbeitssituation. "
                        f"Wenn diese Fragen beantwortet wurden, gibst du Empfehlungen, um die Situation zu verbessern."
                        f"Die folgende Frage wurde bereits von dir an den User gestellt: "
                        f"Hallo {user_name}, wie geht es Dir heute?"}
        ]

    def create_chat(self, user_message):
        messages = self.initial_message.copy()
        messages.append({"role": "user", "content": user_message})
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return completion.choices[0].message


# Beispiel für die Verwendung
if __name__ == '__main__':
    chat = Chat()
    user_name = "Linus"
    chat.set_initial_message(user_name)
    print(chat.create_chat("Hallo. Ich fühle mich heute nicht so gut. Ich bin gestresst und überfordert."))
