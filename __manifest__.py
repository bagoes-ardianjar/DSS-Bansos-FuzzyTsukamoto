{
    'name': 'SPK Mamdani',
    'version': '13.0.1.0.0',
    'category': '',
    'summary': 'SPK Mamdani',
    'description': """
        Ini adalah module custom tentang SPK Mamdani
    """,
    'website': '',
    'author': 'Bagus',
    'depends': ['web','base'],
    'data': [
                'security/ir.model.access.csv',
                'views/tugas_kuliah_spk_view.xml',
                'views/tugas_kuliah_spk_sequence.xml',
                'views/tugas_kuliah_spk_action.xml',
                'views/tugas_kuliah_spk_menuitem.xml',
            ],
    'installable': True,
    'application': True,
    'license': 'OEEL-1',
}