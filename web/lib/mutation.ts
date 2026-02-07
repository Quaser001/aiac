
export function extractResidueNumber(mutation: string): number | null {
    const match = mutation.match(/[A-Z](\d+)[A-Z]/);
    if (!match) return null;
    return parseInt(match[1], 10);
}
