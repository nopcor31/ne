import React from 'react';
import {
  LayoutDashboard,
  Users,
  DollarSign,
  FileText,
  Calendar,
  Building2,
  PackageCheck,
  Receipt,
  Bell,
  History,
  Settings,
  Code,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';

export type TabType =
  | 'dashboard'
  | 'clientes'
  | 'tarifas'
  | 'cotizaciones'
  | 'programacion'
  | 'areas'
  | 'ordenes'
  | 'facturacion'
  | 'alertas'
  | 'historial'
  | 'configuracion'
  | 'auditoria';

interface SidebarProps {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
  collapsed: boolean;
  setCollapsed: (val: boolean) => void;
  alertCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  collapsed,
  setCollapsed,
  alertCount,
}) => {
  const menuItems = [
    { id: 'dashboard' as TabType, label: 'Dashboard', icon: LayoutDashboard },
    { id: 'clientes' as TabType, label: 'Clientes (CRM)', icon: Users },
    { id: 'tarifas' as TabType, label: 'Tarifas & Catálogo', icon: DollarSign },
    { id: 'cotizaciones' as TabType, label: 'Cotizaciones', icon: FileText },
    { id: 'programacion' as TabType, label: 'Programación', icon: Calendar },
    { id: 'areas' as TabType, label: 'Áreas Médicas', icon: Building2 },
    { id: 'ordenes' as TabType, label: 'Órdenes de Compra', icon: PackageCheck },
    { id: 'facturacion' as TabType, label: 'Facturación', icon: Receipt },
    { id: 'alertas' as TabType, label: 'Alertas Operativas', icon: Bell, badge: alertCount },
    { id: 'historial' as TabType, label: 'Historial / Bitácora', icon: History },
    { id: 'configuracion' as TabType, label: 'Configuración', icon: Settings },
    { id: 'auditoria' as TabType, label: 'Auditoría de Código', icon: Code, badgeText: 'Python' },
  ];

  return (
    <aside
      className={`bg-slate-900 text-slate-300 flex flex-col transition-all duration-200 border-r border-slate-800 relative z-20 ${
        collapsed ? 'w-16' : 'w-64'
      }`}
    >
      {/* Brand Header */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-slate-800">
        {!collapsed && (
          <div className="flex items-center gap-2.5 overflow-hidden">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center font-black text-white text-sm shadow-md">
              NE
            </div>
            <div>
              <h1 className="text-sm font-bold text-white tracking-tight leading-none">CRM Operativo</h1>
              <p className="text-[10px] text-slate-400 font-medium mt-0.5">Servicios Médicos NE</p>
            </div>
          </div>
        )}

        {collapsed && (
          <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center font-black text-white text-sm mx-auto">
            NE
          </div>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 hidden md:block"
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto p-2 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;

          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-colors relative ${
                isActive
                  ? 'bg-blue-600 text-white font-semibold shadow-sm'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
              }`}
              title={collapsed ? item.label : undefined}
            >
              <Icon className="w-4 h-4 shrink-0" />
              {!collapsed && <span className="truncate">{item.label}</span>}

              {item.badge !== undefined && item.badge > 0 && (
                <span
                  className={`ml-auto text-[10px] font-bold px-1.5 py-0.5 rounded-full ${
                    isActive ? 'bg-white text-blue-700' : 'bg-rose-500 text-white'
                  }`}
                >
                  {item.badge}
                </span>
              )}

              {item.badgeText && !collapsed && (
                <span className="ml-auto text-[9px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  {item.badgeText}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer Info */}
      {!collapsed && (
        <div className="p-3 border-t border-slate-800 text-[11px] text-slate-500 flex items-center justify-between">
          <span>v2.0 Arquitectura</span>
          <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">PySide6</span>
        </div>
      )}
    </aside>
  );
};
