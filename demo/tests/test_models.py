from odoo.tests import TransactionCase, Like
from psycopg2.errors import NotNullViolation
from odoo.tools import mute_logger


class TestHobby(TransactionCase):
    def test_name(self):
        hobby = self.env['demo.hobby'].create({
            'name': 'Programming'
        })
        self.assertEqual(hobby.name, 'Programming')

    def test_name_is_required(self):
        with self.assertRaises(NotNullViolation):
            with mute_logger('odoo.sql_db'):
                self.env['demo.hobby'].create({})


class TestUsers(TransactionCase):

    def tearDown(self):
        super().tearDown()
        self.env.flush_all()

    def test_description_is_required(self):
        with mute_logger('odoo.sql_db'):
            with self.assertRaises(Exception):
                user = self.env['res.users'].create({
                    'name': 'Marie-Noël',
                    'login': 'mnv',
                })
                user.description = None


    def test_description_one_line(self):
        with self.assertRaises(ValueError) as error_catcher:
            self.env['res.users'].create({
                'name': 'Jeremy',
                'login': 'jem',
                'description': 'I like \n Sports'
            })
        self.assertEqual(error_catcher.exception.args[0], Like("Description must be oneline ..."))

    def test_hobby(self):
        minecraft = self.env.ref('demo.hobby_minecraft')
        user = self.env['res.users'].create({
            'name': 'Pierre',
            'login': 'pie',
            'hobby': minecraft.id
        })
        self.assertEqual(user.hobby.name, 'Minecraft')
