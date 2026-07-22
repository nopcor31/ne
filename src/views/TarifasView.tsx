import React, { useState } from 'react';
import { Tarifa, Ciudad, Servicio, Cliente, TipoDia, TipoHorario, TipoCliente } from '../types';
import { DollarSign, Plus, Filter, ShieldCheck, Upload, Building } from 'lucide-react';

interface TarifasViewProps {
  tarifas: Tarifa[];
  ciudades: Ciudad[];
  servicios: Servicio[];
  clientes: Cliente[];
  onAddTarifa: (nueva: Partial<Tarifa>) => void;
}

export const TarifasView: React.FC<TarifasViewProps> = ({
  tarifas,
  ciudades,
  servicios,
  clientes,
  onAddTarifa,
}) => {
  const [filterCiudad, setFilterCiudad] = useState<number | 'TODAS'>('TODAS');
  const [filterCliente, setFilterCliente] = useState<string>('TODOS');
  const [showModal, setShowModal] = useState(false);

  const [newTarifa, setNewTarifa] = useState<Partial<Tarifa>>({
    ciudadId: 1,
    servicioId: 1,
    tipoDia: TipoDia.ORDINARIO,
    tipoHorario: TipoHorario.DIURNO,
    clienteId: null,
    valorHora: 300000,
    vigenteDesde: new Date().toISOString().split('T')[0],
    activo: true,
  });

  const getCiudadNombre = (id: number) => ciudades.find((c) => c.id === id)?.nombre || 'Ciudad';
  const getServicioNombre = (id: number) => servicios.find((s) => s.id === id)?.nombre || 'Servicio';
  const getClienteNombre = (id: number | null) => {
    if (id === null) return 'TARIFARIO GENERAL';
    return clientes.find((c) => c.id === id)?.empresa || 'Cliente Especial';
  };

  const filteredTarifas = tarifas.filter((t) => {
    if (filterCiudad !== 'TODAS' && t.ciudadId !== filterCiudad) return false;
    if (filterCliente === 'GENERAL' && t.clienteId !== null) return false;
    if (filterCliente === 'ESPECIAL' && t.clienteId === null) return false;
    return true;
  });

  const handleSaveTarifa = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTarifa.valorHora || newTarifa.valorHora <= 0) return;
    onAddTarifa(newTarifa);
    setShowModal(false);
    setNewTarifa({
      ciudadId: 1,
      servicioId: 1,
      tipoDia: TipoDia.ORDINARIO,
      tipoHorario: TipoHorario.DIURNO,
      clienteId: null,
      valorHora: 300000,
      vigenteDesde: new Date().toISOString().split('T')[0],
      activo: true,
    });
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-600" />
            Catálogo de Tarifas y Strategy de Precios
          </h2>
          <p className="text-xs text-slate-500">
            Matriz de tarifas por hora según ciudad, tipo de día (Ordinario/Festivo), franja horaria y tarifas exclusivas de clientes.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => alert('Simulación de importación masiva CSV de tarifas completada.')}
            className="bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium text-xs px-3 py-2 rounded-lg flex items-center gap-1.5"
          >
            <Upload className="w-4 h-4" /> Importar CSV
          </button>

          <button
            onClick={() => setShowModal(true)}
            className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-xs"
          >
            <Plus className="w-4 h-4" /> Nueva Tarifa
          </button>
        </div>
      </div>

      {/* Filter Strip */}
      <div className="flex flex-wrap items-center gap-3 bg-slate-50 p-3 rounded-xl border border-slate-200 text-xs">
        <div className="flex items-center gap-1.5 font-bold text-slate-700">
          <Filter className="w-4 h-4 text-slate-400" /> Filtros:
        </div>

        <div>
          <select
            value={filterCiudad}
            onChange={(e) =>
              setFilterCiudad(e.target.value === 'TODAS' ? 'TODAS' : Number(e.target.value))
            }
            className="p-1.5 bg-white border border-slate-200 rounded-lg"
          >
            <option value="TODAS">Todas las Ciudades</option>
            {ciudades.map((c) => (
              <option key={c.id} value={c.id}>
                {c.nombre}
              </option>
            ))}
          </select>
        </div>

        <div>
          <select
            value={filterCliente}
            onChange={(e) => setFilterCliente(e.target.value)}
            className="p-1.5 bg-white border border-slate-200 rounded-lg"
          >
            <option value="TODOS">Todas las Tarifas</option>
            <option value="GENERAL">Solo Tarifario General</option>
            <option value="ESPECIAL">Solo Clientes Especiales</option>
          </select>
        </div>
      </div>

      {/* Tariff Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-100 text-slate-600 font-semibold border-b border-slate-200">
                <th className="p-3 pl-4">Tipo de Tarifa</th>
                <th className="p-3">Ciudad</th>
                <th className="p-3">Servicio</th>
                <th className="p-3">Tipo Día</th>
                <th className="p-3">Franja Horaria</th>
                <th className="p-3 text-right">Valor Hora (COP)</th>
                <th className="p-3">Vigencia Desde</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {filteredTarifas.map((t) => (
                <tr key={t.id} className="hover:bg-slate-50 transition-colors">
                  <td className="p-3 pl-4">
                    {t.clienteId ? (
                      <span className="font-bold text-amber-800 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded text-[10px] inline-flex items-center gap-1">
                        <Building className="w-3 h-3" />
                        {getClienteNombre(t.clienteId)}
                      </span>
                    ) : (
                      <span className="font-bold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded text-[10px]">
                        TARIFARIO GENERAL
                      </span>
                    )}
                  </td>
                  <td className="p-3 font-medium text-slate-900">{getCiudadNombre(t.ciudadId)}</td>
                  <td className="p-3 font-semibold">{getServicioNombre(t.servicioId)}</td>
                  <td className="p-3">
                    {t.tipoDia === TipoDia.FESTIVO ? (
                      <span className="font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded text-[10px]">
                        FESTIVO / DOMINGO
                      </span>
                    ) : (
                      <span className="text-slate-600 font-medium">ORDINARIO</span>
                    )}
                  </td>
                  <td className="p-3">
                    {t.tipoHorario === TipoHorario.NOCTURNO ? (
                      <span className="font-bold text-purple-700 bg-purple-50 px-2 py-0.5 rounded text-[10px]">
                        NOCTURNO (19:00-06:59)
                      </span>
                    ) : (
                      <span className="font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded text-[10px]">
                        DIURNO (07:00-18:59)
                      </span>
                    )}
                  </td>
                  <td className="p-3 text-right font-black text-slate-900 text-sm">
                    ${t.valorHora.toLocaleString('es-CO')}
                  </td>
                  <td className="p-3 text-slate-500 font-mono text-[11px]">{t.vigenteDesde}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal Nueva Tarifa */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-md p-6">
            <h3 className="text-base font-bold text-slate-900 mb-4">Agregar Nueva Tarifa al Catálogo</h3>
            <form onSubmit={handleSaveTarifa} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Destinatario / Ámbito</label>
                <select
                  value={newTarifa.clienteId === null ? 'GENERAL' : newTarifa.clienteId}
                  onChange={(e) =>
                    setNewTarifa({
                      ...newTarifa,
                      clienteId: e.target.value === 'GENERAL' ? null : Number(e.target.value),
                    })
                  }
                  className="w-full p-2 border border-slate-200 rounded-lg"
                >
                  <option value="GENERAL">Tarifario General (Publico)</option>
                  {clientes
                    .filter((c) => c.tipoCliente === TipoCliente.ESPECIAL)
                    .map((c) => (
                      <option key={c.id} value={c.id}>
                        Cliente Especial: {c.empresa}
                      </option>
                    ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Ciudad</label>
                  <select
                    value={newTarifa.ciudadId}
                    onChange={(e) => setNewTarifa({ ...newTarifa, ciudadId: Number(e.target.value) })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  >
                    {ciudades.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.nombre}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Servicio</label>
                  <select
                    value={newTarifa.servicioId}
                    onChange={(e) => setNewTarifa({ ...newTarifa, servicioId: Number(e.target.value) })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  >
                    {servicios.map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.nombre}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Tipo de Día</label>
                  <select
                    value={newTarifa.tipoDia}
                    onChange={(e) => setNewTarifa({ ...newTarifa, tipoDia: e.target.value as TipoDia })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  >
                    <option value={TipoDia.ORDINARIO}>ORDINARIO (Lunes-Sábado)</option>
                    <option value={TipoDia.FESTIVO}>FESTIVO / DOMINGO</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Franja Horaria</label>
                  <select
                    value={newTarifa.tipoHorario}
                    onChange={(e) =>
                      setNewTarifa({ ...newTarifa, tipoHorario: e.target.value as TipoHorario })
                    }
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  >
                    <option value={TipoHorario.DIURNO}>DIURNO (07:00 - 18:59)</option>
                    <option value={TipoHorario.NOCTURNO}>NOCTURNO (19:00 - 06:59)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Valor Hora (COP)</label>
                <input
                  type="number"
                  required
                  step="5000"
                  value={newTarifa.valorHora}
                  onChange={(e) => setNewTarifa({ ...newTarifa, valorHora: Number(e.target.value) })}
                  className="w-full p-2 border border-slate-200 rounded-lg font-mono text-sm font-bold"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-200">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-3 py-2 bg-slate-100 text-slate-700 font-semibold rounded-lg"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-emerald-600 text-white font-semibold rounded-lg"
                >
                  Guardar Tarifa
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
