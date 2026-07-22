import React from 'react';
import { Search, Plus, User } from 'lucide-react';
import { Alerta } from '../types';
import { AlertBell } from './AlertBell';

interface TopbarProps {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  alertas: Alerta[];
  onMarkAsRead: (id: number) => void;
  onNavigateToAlert: (alerta: Alerta) => void;
  onNewQuotation: () => void;
}

export const Topbar: React.FC<TopbarProps> = ({
  searchQuery,
  setSearchQuery,
  alertas,
  onMarkAsRead,
  onNavigateToAlert,
  onNewQuotation,
}) => {
  return (
    <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between gap-4 sticky top-0 z-30 shadow-2xs">
      {/* Global Search */}
      <div className="flex-1 max-w-md relative">
        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Buscar clientes, cotizaciones (COT-2026-...), eventos o facturas..."
          className="w-full pl-9 pr-4 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all text-slate-800 placeholder:text-slate-400"
        />
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3">
        <button
          onClick={onNewQuotation}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-xs transition-colors"
        >
          <Plus className="w-4 h-4" />
          Nueva Cotización
        </button>

        <div className="h-5 w-px bg-slate-200" />

        <AlertBell
          alertas={alertas}
          onMarkAsRead={onMarkAsRead}
          onNavigateToAlert={onNavigateToAlert}
        />

        <div className="h-5 w-px bg-slate-200" />

        {/* User Info */}
        <div className="flex items-center gap-2.5 pl-1">
          <div className="w-8 h-8 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-700">
            <User className="w-4 h-4" />
          </div>
          <div className="hidden sm:block text-left">
            <p className="text-xs font-semibold text-slate-800 leading-tight">Admin Tech Lead</p>
            <p className="text-[10px] text-slate-500">Coordinación Operativa</p>
          </div>
        </div>
      </div>
    </header>
  );
};
