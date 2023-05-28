import openai as openai


class OpenAIGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_text(self, prompt):
        test_prompt = "how much is 4 + 3"

        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=prompt,
          # prompt=test_prompt,
          temperature=0.9,
          max_tokens=50,
          top_p=1,
          frequency_penalty=0.0,
          presence_penalty=0.6,
          stop=[" Human:", " AI:"]
        )

        to_return = self.print_text(response)
        return to_return

    @staticmethod
    def print_text(my_response):
        my_text = my_response.choices[0].text.strip()
        # print('AI:', my_text)
        return my_text
