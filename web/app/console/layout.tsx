"use client";

import { Sidebar } from "@/components/Sidebar";
import { ConsoleProvider } from "@/context/ConsoleContext";
import { useState } from "react";
import { cn } from "@/lib/utils";

export default function ConsoleLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const [collapsed, setCollapsed] = useState(false);

    return (
        <ConsoleProvider>
            <div className="flex min-h-screen pt-16">
                <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />
                <div className={cn(
                    "flex-1 transition-all duration-300",
                    collapsed ? "lg:pl-20" : "lg:pl-64"
                )}>
                    <div className="p-8 max-w-[1600px] mx-auto">
                        {children}
                    </div>
                </div>
            </div>
        </ConsoleProvider>
    );
}
