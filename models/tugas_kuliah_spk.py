from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError

class penduduk_indonesia(models.Model):
    _name = 'penduduk.indonesia'

    name = fields.Char(string="KK")
    nama_kepala_keluarga = fields.Char(string="Nama")
    ktp = fields.Char(string="KTP")
    tanggal_lahir = fields.Date(string="Tanggal Lahir")
    penghasilan = fields.Float(string="Penghasilan / bulan", default=0.0)
    pengeluaran = fields.Float(string="Pengeluaran / bulan", default=0.0)
    hasil_kelayakan = fields.Char(string="Hasil Kelayakan")
    sudah_dihitung = fields.Boolean(default=False)

class parameter_penghasilan_mamdani(models.Model):
    _name = 'parameter.penghasilan.mamdani'

    @api.model
    def create(self, vals):
        res = super(parameter_penghasilan_mamdani, self).create(vals)
        for rec in res:
            seq = self.env['ir.sequence'].next_by_code('parameter.penghasilan.mamdani', sequence_date=rec.create_date) or '/'
            rec.name = seq
        return res

    name = fields.Char(string="Name", default="New")
    penghasilan_sedikit_range_awal = fields.Float(string="Penghasilan Sedikit Range Awal", default=0.0)
    penghasilan_sedikit_range_akhir = fields.Float(string="Penghasilan Sedikit Range Akhir", default=0.0)
    penghasilan_cukup_range_awal = fields.Float(string="Penghasilan Cukup Range Awal", default=0.0)
    penghasilan_cukup_range_akhir = fields.Float(string="Penghasilan Cukup Range Akhir", default=0.0)
    penghasilan_banyak_range_awal = fields.Float(string="Penghasilan Banyak Range Awal", default=0.0)
    penghasilan_banyak_range_akhir = fields.Float(string="Penghasilan Banyak Range Akhir", default=0.0)
    derajat_keanggotaan_max = fields.Float(string="Derajat Keanggotaan Max", default=0.0)
    derajat_keanggotaan_min = fields.Float(string="Derajat Keanggotaan Min", default=0.0)


class parameter_pengeluaran_mamdani(models.Model):
    _name = 'parameter.pengeluaran.mamdani'

    @api.model
    def create(self, vals):
        res = super(parameter_pengeluaran_mamdani, self).create(vals)
        for rec in res:
            seq = self.env['ir.sequence'].next_by_code('parameter.pengeluaran.mamdani', sequence_date=rec.create_date) or '/'
            rec.name = seq
        return res

    name = fields.Char(string="Name", default="New")
    pengeluaran_sedikit_range_awal = fields.Float(string="Pengeluaran Sedikit Range Awal", default=0.0)
    pengeluaran_sedikit_range_akhir = fields.Float(string="Pengeluaran Sedikit Range Akhir", default=0.0)
    pengeluaran_cukup_range_awal = fields.Float(string="Pengeluaran Cukup Range Awal", default=0.0)
    pengeluaran_cukup_range_akhir = fields.Float(string="Pengeluaran Cukup Range Akhir", default=0.0)
    pengeluaran_banyak_range_awal = fields.Float(string="Pengeluaran Banyak Range Awal", default=0.0)
    pengeluaran_banyak_range_akhir = fields.Float(string="Pengeluaran Banyak Range Akhir", default=0.0)
    derajat_keanggotaan_max = fields.Float(string="Derajat Keanggotaan Max", default=0.0)
    derajat_keanggotaan_min = fields.Float(string="Derajat Keanggotaan Min", default=0.0)


class hitung_kelayakan(models.Model):
    _name = 'hitung.kelayakan'

    @api.onchange('kk')
    def func_onchange_kk(self):
        if not self.kk:
            return {}
        else:
            self.nama_warga = self.kk.nama_kepala_keluarga
            self.penghasilan = self.kk.penghasilan
            self.pengeluaran = self.kk.pengeluaran
        return {}


    def func_hitung(self):
        hasil_sed_r_akhir = self.parameter_penghasilan_id.penghasilan_sedikit_range_akhir
        hasil_cuk_r_awal = self.parameter_penghasilan_id.penghasilan_cukup_range_awal
        keluar_sed_r_akhir = self.parameter_pengeluaran_id.pengeluaran_sedikit_range_akhir
        keluar_cuk_r_awal = self.parameter_pengeluaran_id.pengeluaran_cukup_range_awal

        thp_hasil_sedikit = (hasil_sed_r_akhir - self.penghasilan) / (hasil_sed_r_akhir - hasil_cuk_r_awal)
        thp_hasil_cukup = (self.penghasilan - hasil_cuk_r_awal) / (hasil_sed_r_akhir - hasil_cuk_r_awal)

        thp_keluar_sedikit = (keluar_sed_r_akhir - self.pengeluaran) / (keluar_sed_r_akhir - keluar_cuk_r_awal)
        thp_keluar_cukup = (self.pengeluaran - keluar_cuk_r_awal) / (keluar_sed_r_akhir - keluar_cuk_r_awal)

        if thp_hasil_sedikit <= thp_keluar_sedikit:
            predikat_1 = thp_hasil_sedikit
        else:
            predikat_1 = thp_keluar_sedikit

        if thp_hasil_sedikit <= thp_keluar_cukup:
            predikat_2 = thp_hasil_sedikit
        else:
            predikat_2 = thp_keluar_cukup

        if thp_hasil_cukup <= thp_keluar_sedikit:
            predikat_3 = thp_hasil_cukup
        else:
            predikat_3 = thp_keluar_sedikit

        if thp_hasil_cukup <= thp_keluar_cukup:
            predikat_4 = thp_hasil_cukup
        else:
            predikat_4 = thp_keluar_cukup

        nilai_z1 = 40 + ((60 - 40) * predikat_1)
        nilai_z2 = 60 - ((60 - 40) * predikat_2)
        nilai_z3 = 40 + ((60 - 40) * predikat_3)
        nilai_z4 = 60 - ((60 - 40) * predikat_4)
        nilai_akhir = ((predikat_1 * nilai_z1) + (predikat_2 * nilai_z2) + (predikat_3 * nilai_z3) + (predikat_4 * nilai_z4)) / (predikat_1 + predikat_2 + predikat_3 + predikat_4)
        self.kk.hasil_kelayakan = nilai_akhir
        if nilai_akhir > 50:
            keterangan = "Kelayakan Tinggi"
        else:
            keterangan = "Kelayakan Rendah"
        form_view_id = self.env['ir.model.data'].xmlid_to_res_id('tugas_kuliah_spk.form_wiz_keterangan_id')
        vals_ket = {
            'name': 'Hasil Hitung',
            'keterangan': keterangan,
            'hitung_kelayakan_id': self.id
        }
        new_hasil = self.env['result.kelayakan'].create(vals_ket)
        return {
            'name': "Hasil Hitung",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'result.kelayakan',
            'views': [[form_view_id, 'form']],
            'target': 'new',
            'res_id': new_hasil.id
        }

    name = fields.Char(string="Name", default="Hitung")
    kk = fields.Many2one('penduduk.indonesia', string="KK")
    nama_warga = fields.Char(string="Nama Warga")
    penghasilan = fields.Float(string="Penghasilan / bulan", default=0.0)
    pengeluaran = fields.Float(string="Pengeluaran / bulan", default=0.0)
    parameter_penghasilan_id = fields.Many2one('parameter.penghasilan.mamdani')
    parameter_pengeluaran_id = fields.Many2one('parameter.pengeluaran.mamdani')


class result_kelayakan(models.TransientModel):
    _name = 'result.kelayakan'

    name = fields.Char(default="Result")
    keterangan = fields.Char(string="Keterangan")
    hitung_kelayakan_id = fields.Many2one('hitung.kelayakan')