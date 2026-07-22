import React from 'react';
import { Programacion, Cotizacion, Cliente } from '../types';
import { Calendar, RefreshCw, CheckCircle, Clock, MapPin, UserCheck, Check } from 'lucide-react';

interface ProgramacionViewProps {
  programaciones: Programacion[];
  cotizaciones: Cotizacion[];
  clientes: Cliente[];
  onSyncOutlook: () => void;
}

export const ProgramacionView: React.FC<ProgramacionViewProps> = ({
  programaciones,
  cotizaciones,
  clientes,
  onSyncOutlook,
}) => {
  const getCotizacionNum = (id: number) =>
    cotizaciones.find((c) => c.id === id)?.numeroCotizacion || 'COT-0000';

  const getClienteName = (cotId: number) => {
    const cot = cotizaciones.find((c) => c.id === cotId);
    if (!cot) return 'Cliente';
    return clientes.find((c) => c.id === cot.clienteId)?.empresa || 'Cliente';
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-cyan-600" />
            Programación Operativa de Servicios
          </h2>
          <p className="text-xs text-slate-500">
            Agenda de ambulancias, paramédicos y médicos con sincronización automática a Microsoft Outlook Calendar.
          </p>
        </div>

        <button
          onClick={onSyncOutlook}
          className="bg-cyan-600 hover:bg-cyan-700 text-white font-semibold text-xs px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-xs"
        >
          <RefreshCw className="w-4 h-4" /> Sincronizar Outlook Calendar
        </button>
      </div>

      {/* Schedule Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-100 text-slate-600 font-semibold border-b border-slate-200">
                <th className="p-3 pl-4">Cotización</th>
                <th className="p-3">Cliente</th>
                <th className="p-3">Fecha & Horario</th>
                <th className="p-3">Recurso Asignado</th>
                <th className="p-3">Estado Programación</th>
                <th className="p-3">Outlook Event ID</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {programaciones.map((p) => (
                <tr key={p.id} className="hover:bg-slate-50 transition-colors">
                  <td className="p-3 pl-4 font-bold text-blue-700 font-mono">{getCotizacionNum(p.cotizacionId)}</td>
                  <td className="p-3 font-semibold text-slate-900">{getClienteName(p.cotizacionId)}</td>
                  <td className="p-3">
                    <p className="font-bold text-slate-800">{p.fechaProgramada}</p>
                    <p className="text-[10px] text-slate-400">{p.horaInicio} - {p.horaFin}</p>
                  </td>
                  <td className="p-3 font-medium text-slate-800 flex items-center gap-1.5">
                    <UserCheck className="w-3.5 h-3.5 text-cyan-600 shrink-0" />
                    {p.recursoAsignado || 'Pendiente Asignación'}
                  </td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-cyan-100 text-cyan-800 border border-cyan-300">
                      {p.estado}
                    </span>
                  </td>
                  <td className="p-3 font-mono text-[10px] text-slate-400">
                    {p.outlookEventId ? (
                      <span className="text-emerald-700 font-bold flex items-center gap-1">
                        <Check className="w-3 h-3 text-emerald-600" /> Synced ({p.outlookEventId.slice(0, 12)}...)
                      </span>
                    ) : (
                      'No sincronizado'
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
