import os
import unittest

from dotenv import load_dotenv
import pandas as pd

from neo4j_runway import Discovery, GraphDataModeler, LLM, DataModel


load_dotenv()


class TestLLMGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def test_sequence_with_countries_data(self) -> None:
        USER_GENERATED_INPUT = {
            "general_description": "This is data on different countries.",
            "id": "unique id for a country.",
            "name": "the country name.",
            "phone_code": "country area code.",
            "capital": "the capital of the country.",
            "currency_name": "name of the country's currency.",
            "region": "primary region of the country.",
            "subregion": "subregion location of the country.",
            "timezones": "timezones contained within the country borders.",
            "latitude": "the latitude coordinate of the country center. should be part of node key.",
            "longitude": "the longitude coordinate of the country center. should be part of node key.",
        }

        # test discovery generation
        data = pd.read_csv("neo4j_runway/tests/resources/countries.csv")
        disc = Discovery(data=data, llm=LLM(), user_input=USER_GENERATED_INPUT)

        disc.run(show_result=False)

        self.assertIsInstance(disc.discovery, str)

        # test data modeler
        gdm = GraphDataModeler(llm=LLM(model="gpt-4o-2024-05-13"), discovery=disc)
        gdm.create_initial_model()

        self.assertIsInstance(gdm.current_model, DataModel)

    def test_sequence_with_pets_data(self) -> None:

        # test discovery generation
        data = pd.read_csv("neo4j_runway/tests/resources/pets.csv")
        disc = Discovery(data=data, llm=LLM())

        disc.run(show_result=False)

        self.assertIsInstance(disc.discovery, str)

        # test data modeler
        gdm = GraphDataModeler(llm=LLM(model="gpt-4o-2024-05-13"), discovery=disc)
        gdm.create_initial_model()

        self.assertIsInstance(gdm.current_model, DataModel)
