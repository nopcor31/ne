import React, { useState } from 'react';
import { ConfiguracionSistema, Festivo } from '../types';
import { Settings, Save, Calendar, Building, Mail, Shield } from 'lucide-react';

interface ConfiguracionViewProps {
  config: ConfiguracionSistema;
  festivos: Festivo[];
  onSaveConfig: (updated: ConfiguracionSistema) => void;
  onAddFestivo: (fecha: string, nombre: string) => void;
}

export const ConfiguracionView: React.FC<ConfiguracionViewProps> = ({
  config,
  festivos,
  onSaveConfig,
  onAddFestivo,
}) => {
  const [formData, setFormData] = useState<ConfiguracionSistema>(config);
  const [newFestivoFecha, setNewFestivoFecha] = useState('');
  const [newFestivoNombre, setNewFestivoNombre] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSaveConfig(formData);
    alert('Configuración del sistema actualizada correctamente.');
  };

  const handleAddFestivoSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFestivoFecha || !newFestivoNombre) return;
    onAddFestivo(newFestivoFecha, newFestivoNombre);
    setNewFestivoFecha('');
    setNewFestivoNombre('');
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Settings className="w-5 h-5 text-slate-700" />
            Parámetros del Sistema y Calendario Legal
          </h2>
          <p className="text-xs text-slate-500">
            Ajustes globales de la empresa, datos institucionales, plantilla PDF y días festivos legales de Colombia.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Company Settings */}
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4 text-xs">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-200 pb-2">
            Datos de la Institución
          </h3>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Nombre / Razón Social</label>
            <input
              type="text"
              value={formData.empresaNombre}
              onChange={(e) => setFormData({ ...formData, empresaNombre: e.target.value })}
              className="w-full p-2 border border-slate-200 rounded-lg"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">NIT</label>
              <input
                type="text"
                value={formData.empresaNit}
                onChange={(e) => setFormData({ ...formData, empresaNit: e.target.value })}
                className="w-full p-2 border border-slate-200 rounded-lg font-mono"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Teléfono Institucional</label>
              <input
                type="text"
                value={formData.empresaTelefono}
                onChange={(e) => setFormData({ ...formData, empresaTelefono: e.target.value })}
                className="w-full p-2 border border-slate-200 rounded-lg"
              />
            </div>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Dirección Principal</label>
            <input
              type="text"
              value={formData.empresaDireccion}
              onChange={(e) => setFormData({ ...formData, empresaDireccion: e.target.value })}
              className="w-full p-2 border border-slate-200 rounded-lg"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Cuenta Outlook Envío Automático</label>
            <input
              type="email"
              value={formData.outlookCuentaEmail}
              onChange={(e) => setFormData({ ...formData, outlookCuentaEmail: e.target.value })}
              className="w-full p-2 border border-slate-200 rounded-lg font-mono"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1">Condiciones Comerciales PDF</label>
            <textarea
              rows={4}
              value={formData.pdfCondicionesGenerales}
              onChange={(e) => setFormData({ ...formData, pdfCondicionesGenerales: e.target.value })}
              className="w-full p-2 border border-slate-200 rounded-lg font-mono text-[11px]"
            />
          </div>

          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs px-4 py-2 rounded-lg flex items-center gap-1.5 shadow-xs"
          >
            <Save className="w-4 h-4" /> Guardar Cambios
          </button>
        </form>

        {/* Holiday Calendar Management */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4 text-xs">
          <h3 className="text-sm font-bold text-slate-900 border-b border-slate-200 pb-2">
            Gestión de Días Festivos Legales
          </h3>

          <form onSubmit={handleAddFestivoSubmit} className="flex gap-2">
            <input
              type="date"
              required
              value={newFestivoFecha}
              onChange={(e) => setNewFestivoFecha(e.target.value)}
              className="p-2 border border-slate-200 rounded-lg"
            />
            <input
              type="text"
              required
              placeholder="Nombre del festivo (ej: San Pedro)"
              value={newFestivoNombre}
              onChange={(e) => setNewFestivoNombre(e.target.value)}
              className="flex-1 p-2 border border-slate-200 rounded-lg"
            />
            <button type="submit" className="bg-slate-900 text-white font-semibold px-3 py-2 rounded-lg">
              + Agregar
            </button>
          </form>

          <div className="max-h-80 overflow-y-auto space-y-1.5 border border-slate-200 rounded-lg p-2 divide-y divide-slate-100">
            {festivos.map((f) => (
              <div key={f.id} className="pt-1.5 flex items-center justify-between text-xs">
                <span className="font-mono font-bold text-slate-800">{f.fecha}</span>
                <span className="font-medium text-slate-700">{f.nombre}</span>
                <span className="text-[9px] bg-slate-100 text-slate-500 font-bold px-1.5 py-0.5 rounded">
                  {f.origen}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
