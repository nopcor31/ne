import React from 'react';
import { Cotizacion, Cliente } from '../types';
import { StateBadge } from './StateBadge';
import { ESTADO_LABELS, obtenerProximosEstados } from '../services/stateMachine';
import { Calendar, Building, DollarSign, ArrowRight, Eye } from 'lucide-react';

interface KanbanBoardProps {
  cotizaciones: Cotizacion[];
  clientes: Cliente[];
  onSelectCotizacion: (cot: Cotizacion) => void;
  onStateTransition: (cotId: number, nextEstado: any) => void;
}

export const KanbanBoard: React.FC<KanbanBoardProps> = ({
  cotizaciones,
  clientes,
  onSelectCotizacion,
  onStateTransition,
}) => {
  const getClienteName = (id: number) => {
    return clientes.find((c) => c.id === id)?.empresa || 'Cliente Desconocido';
  };

  // Group cotizaciones by state
  const states = Object.keys(ESTADO_LABELS) as any[];

  return (
    <div className="flex gap-4 overflow-x-auto pb-4 pt-1 min-h-[600px] select-none">
      {states.map((estado) => {
        const items = cotizaciones.filter((c) => c.estado === estado);
        const columnTitle = ESTADO_LABELS[estado];

        return (
          <div
            key={estado}
            className="w-72 shrink-0 bg-slate-100/80 rounded-xl border border-slate-200/80 flex flex-col max-h-[750px]"
          >
            {/* Column Header */}
            <div className="p-3 border-b border-slate-200 bg-slate-50/90 rounded-t-xl flex items-center justify-between sticky top-0 z-10">
              <h4 className="text-xs font-bold text-slate-800 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-600" />
                {columnTitle}
              </h4>
              <span className="text-xs font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded-full">
                {items.length}
              </span>
            </div>

            {/* Column Cards */}
            <div className="p-2.5 overflow-y-auto space-y-2.5 flex-1">
              {items.length === 0 ? (
                <div className="p-4 text-center text-xs text-slate-400 border border-dashed border-slate-200 rounded-lg">
                  Sin registros
                </div>
              ) : (
                items.map((cot) => {
                  const nextStates = obtenerProximosEstados(cot.estado);

                  return (
                    <div
                      key={cot.id}
                      className="bg-white rounded-lg border border-slate-200 p-3 shadow-2xs hover:shadow-md transition-all hover:border-blue-300 group"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-blue-700">{cot.numeroCotizacion}</span>
                        <StateBadge estado={cot.estado} size="sm" />
                      </div>

                      <p className="text-xs font-semibold text-slate-900 mt-1.5 flex items-center gap-1">
                        <Building className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                        <span className="truncate">{getClienteName(cot.clienteId)}</span>
                      </p>

                      <div className="mt-2.5 pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
                        <span className="font-bold text-slate-900 flex items-center gap-0.5">
                          <DollarSign className="w-3.5 h-3.5 text-emerald-600" />
                          ${cot.valorTotal.toLocaleString('es-CO')}
                        </span>
                        <span className="text-[10px] text-slate-400 flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {cot.eventos.length} eventos
                        </span>
                      </div>

                      {/* Card Actions */}
                      <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between gap-1">
                        <button
                          onClick={() => onSelectCotizacion(cot)}
                          className="text-[11px] font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1 py-1 px-2 hover:bg-blue-50 rounded"
                        >
                          <Eye className="w-3 h-3" /> Detalle
                        </button>

                        {nextStates.length > 0 && (
                          <div className="flex items-center gap-1">
                            {nextStates.map((ns) => (
                              <button
                                key={ns}
                                onClick={() => onStateTransition(cot.id, ns)}
                                className="text-[10px] font-bold bg-slate-100 hover:bg-blue-600 hover:text-white text-slate-700 px-2 py-1 rounded transition-colors flex items-center gap-1"
                                title={`Pasar a ${ESTADO_LABELS[ns]}`}
                              >
                                {ESTADO_LABELS[ns]} <ArrowRight className="w-2.5 h-2.5" />
                              </button>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
