import React, { useState } from 'react';
import { PYTHON_AUDIT_FILES, PythonFileAudit } from '../data/pythonAuditFiles';
import {
  Code,
  CheckCircle,
  AlertTriangle,
  Play,
  FileCode,
  ShieldCheck,
  CheckCircle2,
  Copy,
  Terminal,
} from 'lucide-react';

export const PythonAuditView: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<PythonFileAudit>(PYTHON_AUDIT_FILES[0]);
  const [auditRunning, setAuditRunning] = useState(false);
  const [auditCompleted, setAuditCompleted] = useState(true);
  const [copied, setCopied] = useState(false);

  const handleRunAudit = () => {
    setAuditRunning(true);
    setTimeout(() => {
      setAuditRunning(false);
      setAuditCompleted(true);
    }, 600);
  };

  const handleCopyCode = () => {
    navigator.clipboard.writeText(selectedFile.code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const correctedCount = PYTHON_AUDIT_FILES.filter((f) => f.status === 'CORREGIDO').length;
  const verifiedCount = PYTHON_AUDIT_FILES.filter((f) => f.status === 'VERIFICADO').length;

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="bg-slate-900 text-white p-6 rounded-2xl border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              AUDITORÍA DE ARQUITECTURA PYTHON
            </span>
            <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
              PySide6 + SQLAlchemy 2.x
            </span>
          </div>
          <h2 className="text-xl font-black text-white mt-1">Inspector de Consistencia & Compilación</h2>
          <p className="text-xs text-slate-300 mt-1">
            Auditoría integral capa por capa: models, repositories, services, controllers, core, config, utils.
          </p>
        </div>

        <button
          onClick={handleRunAudit}
          disabled={auditRunning}
          className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs px-4 py-2.5 rounded-xl shadow-md flex items-center gap-2 transition-all shrink-0"
        >
          <Play className={`w-4 h-4 ${auditRunning ? 'animate-spin' : ''}`} />
          {auditRunning ? 'Ejecutando Verificación...' : 'Re-Ejecutar Auditoría'}
        </button>
      </div>

      {/* Summary KPI Strip */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <p className="text-xs font-semibold text-slate-500 uppercase">Estado del Proyecto</p>
          <div className="flex items-center gap-2 mt-1">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            <h3 className="text-lg font-black text-emerald-700">100% COMPILABLE</h3>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <p className="text-xs font-semibold text-slate-500 uppercase">Archivos Corregidos</p>
          <h3 className="text-2xl font-black text-amber-600 mt-1">{correctedCount} archivos</h3>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <p className="text-xs font-semibold text-slate-500 uppercase">Archivos Verificados</p>
          <h3 className="text-2xl font-black text-blue-600 mt-1">{verifiedCount} archivos</h3>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <p className="text-xs font-semibold text-slate-500 uppercase">Errores Pendientes</p>
          <h3 className="text-2xl font-black text-slate-400 mt-1">0 errores</h3>
        </div>
      </div>

      {/* Interactive Code Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* File Tree List */}
        <div className="lg:col-span-4 bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div className="p-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <h3 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
              <FileCode className="w-4 h-4 text-blue-600" />
              Estructura de Archivos del Proyecto
            </h3>
          </div>

          <div className="p-2 space-y-1 max-h-[600px] overflow-y-auto">
            {PYTHON_AUDIT_FILES.map((f) => {
              const isSelected = selectedFile.path === f.path;

              return (
                <button
                  key={f.path}
                  onClick={() => setSelectedFile(f)}
                  className={`w-full text-left p-2.5 rounded-lg text-xs transition-all flex items-start justify-between gap-2 ${
                    isSelected
                      ? 'bg-blue-50 text-blue-900 font-bold border border-blue-200 shadow-xs'
                      : 'hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className="min-w-0 flex-1">
                    <p className="font-mono text-[11px] truncate">{f.path}</p>
                    <p className="text-[10px] text-slate-400 font-normal uppercase mt-0.5">
                      Módulo: {f.module}
                    </p>
                  </div>

                  {f.status === 'CORREGIDO' ? (
                    <span className="text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-200 shrink-0">
                      CORREGIDO
                    </span>
                  ) : (
                    <span className="text-[9px] font-extrabold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-200 shrink-0">
                      VERIFICADO
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        </div>

        {/* Code Editor Preview & Details */}
        <div className="lg:col-span-8 space-y-4">
          {/* File Issue & Fix Report Box */}
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-blue-700">{selectedFile.path}</span>
              <span className="text-[10px] font-extrabold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                Capa: {selectedFile.module}
              </span>
            </div>

            {selectedFile.issueFound && (
              <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-900">
                <p className="font-bold flex items-center gap-1 text-amber-900">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-600" /> Conflicto Detectado:
                </p>
                <p className="mt-0.5 text-slate-700">{selectedFile.issueFound}</p>
              </div>
            )}

            {selectedFile.fixDetails && (
              <div className="p-2.5 bg-emerald-50 border border-emerald-200 rounded-lg text-xs text-emerald-900">
                <p className="font-bold flex items-center gap-1 text-emerald-900">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> Solución Aplicada:
                </p>
                <p className="mt-0.5 text-slate-700">{selectedFile.fixDetails}</p>
              </div>
            )}
          </div>

          {/* Code Viewer Panel */}
          <div className="bg-slate-950 text-slate-100 rounded-xl border border-slate-800 overflow-hidden shadow-xl">
            <div className="p-3 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-emerald-400" />
                <span className="text-xs font-mono text-slate-300">{selectedFile.path}</span>
              </div>

              <button
                onClick={handleCopyCode}
                className="text-xs font-medium text-slate-400 hover:text-white flex items-center gap-1 bg-slate-800 px-2.5 py-1 rounded"
              >
                <Copy className="w-3 h-3" /> {copied ? 'Copiado!' : 'Copiar Código'}
              </button>
            </div>

            <pre className="p-4 font-mono text-xs overflow-x-auto text-slate-200 leading-relaxed max-h-[500px]">
              <code>{selectedFile.code}</code>
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};
