import React from 'react';
import { AlertTriangle } from 'lucide-react';

export function DisclaimerBanner() {
  return (
    <div className="bg-amber-100 border-b border-amber-300 px-4 py-2 text-sm text-amber-900 flex items-center justify-center gap-2 font-medium">
      <AlertTriangle className="w-4 h-4" />
      <span>
        CAUTION: Investigational Use Only. Not for primary diagnostic decisions.
      </span>
    </div>
  );
}
