import React, { useState } from 'react';
import { Alerta } from '../types';
import { Bell, Check, AlertTriangle, Info, AlertCircle, ExternalLink } from 'lucide-react';

interface AlertBellProps {
  alertas: Alerta[];
  onMarkAsRead: (alertaId: number) => void;
  onNavigateToAlert: (alerta: Alerta) => void;
}

export const AlertBell: React.FC<AlertBellProps> = ({ alertas, onMarkAsRead, onNavigateToAlert }) => {
  const [isOpen, setIsOpen] = useState(false);
  const activeAlerts = alertas.filter((a) => a.activa && !a.fechaVisto);
  const unreadCount = activeAlerts.length;

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors focus:outline-none"
        title="Alertas y Notificaciones"
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 flex h-4 w-4 items-center justify-center rounded-full bg-rose-600 text-[10px] font-bold text-white ring-2 ring-white animate-pulse">
            {unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setIsOpen(false)} />
          <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-xl border border-slate-200 shadow-xl z-50 overflow-hidden animate-in fade-in slide-in-from-top-2 duration-150">
            <div className="p-3 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Bell className="w-4 h-4 text-slate-700" />
                <h4 className="text-sm font-semibold text-slate-800">Alertas Operativas</h4>
                <span className="text-xs font-bold px-2 py-0.5 bg-rose-100 text-rose-700 rounded-full">
                  {unreadCount} sin leer
                </span>
              </div>
            </div>

            <div className="max-h-80 overflow-y-auto divide-y divide-slate-100">
              {alertas.length === 0 ? (
                <div className="p-6 text-center text-xs text-slate-400">No hay alertas activas en el sistema.</div>
              ) : (
                alertas.slice(0, 5).map((alerta) => (
                  <div
                    key={alerta.id}
                    className={`p-3 transition-colors hover:bg-slate-50 flex items-start gap-2.5 ${
                      !alerta.fechaVisto ? 'bg-amber-50/40 font-medium' : ''
                    }`}
                  >
                    <div className="mt-0.5">
                      {alerta.prioridad === 'CRITICA' ? (
                        <AlertCircle className="w-4 h-4 text-rose-600" />
                      ) : alerta.prioridad === 'ADVERTENCIA' ? (
                        <AlertTriangle className="w-4 h-4 text-amber-600" />
                      ) : (
                        <Info className="w-4 h-4 text-blue-600" />
                      )}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className="text-xs font-semibold text-slate-900 truncate">{alerta.titulo}</p>
                        <span className="text-[10px] text-slate-400">
                          {new Date(alerta.fechaCreacion).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                      <p className="text-xs text-slate-600 mt-0.5 line-clamp-2">{alerta.mensaje}</p>

                      <div className="mt-2 flex items-center gap-2">
                        <button
                          onClick={() => {
                            onNavigateToAlert(alerta);
                            setIsOpen(false);
                          }}
                          className="text-[11px] font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1"
                        >
                          Ver detalle <ExternalLink className="w-3 h-3" />
                        </button>
                        {!alerta.fechaVisto && (
                          <button
                            onClick={() => onMarkAsRead(alerta.id)}
                            className="text-[11px] text-slate-500 hover:text-slate-800 flex items-center gap-1"
                          >
                            <Check className="w-3 h-3" /> Marcar leída
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};
