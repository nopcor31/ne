import React from 'react';
import { AreaMedica, Cotizacion, Cliente, EstadoCotizacion } from '../types';
import { Building2, CheckCircle, XCircle, Clock, ShieldCheck } from 'lucide-react';

interface AreasMedicasViewProps {
  areasMedicas: AreaMedica[];
  cotizaciones: Cotizacion[];
  clientes: Cliente[];
  onApproveAreaMedica: (cotId: number, areaId: number) => void;
  onRejectAreaMedica: (cotId: number, areaId: number) => void;
}

export const AreasMedicasView: React.FC<AreasMedicasViewProps> = ({
  areasMedicas,
  cotizaciones,
  clientes,
  onApproveAreaMedica,
  onRejectAreaMedica,
}) => {
  const pendingQuotations = cotizaciones.filter(
    (c) => c.estado === EstadoCotizacion.PENDIENTE_AREA_MEDICA
  );

  const getClienteName = (id: number) => clientes.find((c) => c.id === id)?.empresa || 'Cliente';

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Building2 className="w-5 h-5 text-amber-600" />
            Flujo de Aprobaciones - Áreas Médicas
          </h2>
          <p className="text-xs text-slate-500">
            Revisión técnica de disponibilidad de personal sanitario y equipos antes de programar servicios.
          </p>
        </div>

        <span className="text-xs font-bold px-3 py-1 bg-amber-100 text-amber-800 rounded-full border border-amber-200">
          {pendingQuotations.length} Cotizaciones en espera de dictamen
        </span>
      </div>

      {/* Pending Reviews Grid */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
          Cola de Solicitudes Pendientes
        </h3>

        {pendingQuotations.length === 0 ? (
          <div className="bg-white p-8 rounded-xl border border-slate-200 text-center text-xs text-slate-400">
            ✅ No hay solicitudes pendientes de aprobación médica en este momento.
          </div>
        ) : (
          pendingQuotations.map((cot) => (
            <div key={cot.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono font-bold text-blue-700 text-sm">{cot.numeroCotizacion}</span>
                  <span className="text-xs font-semibold text-slate-900">{getClienteName(cot.clienteId)}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  Total Cobertura: ${cot.valorTotal.toLocaleString('es-CO')} COP · {cot.eventos.length} eventos programados
                </p>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => onRejectAreaMedica(cot.id, 1)}
                  className="bg-rose-50 hover:bg-rose-100 text-rose-700 font-semibold text-xs px-3.5 py-2 rounded-lg border border-rose-200 flex items-center gap-1.5 transition-colors"
                >
                  <XCircle className="w-4 h-4" /> Rechazar
                </button>
                <button
                  onClick={() => onApproveAreaMedica(cot.id, 1)}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs px-4 py-2 rounded-lg shadow-xs flex items-center gap-1.5 transition-colors"
                >
                  <CheckCircle className="w-4 h-4" /> Aprobar Dictamen
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Catalog of Medical Areas */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 space-y-3">
        <h3 className="text-sm font-bold text-slate-800">Catálogo de Áreas Médicas Registradas</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          {areasMedicas.map((area) => (
            <div key={area.id} className="p-3 bg-slate-50 rounded-lg border border-slate-200">
              <p className="font-bold text-slate-900">{area.nombre}</p>
              <p className="text-slate-500">{area.correoContacto} · Tel: {area.telefono}</p>
              <p className="text-slate-600 font-medium mt-1">Responsable: {area.responsable}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
