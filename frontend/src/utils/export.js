/**
 * Export utility functions for generating reports in various formats
 */

/**
 * Export data as CSV
 */
export const exportToCSV = (data, filename = 'export.csv') => {
  if (!data || data.length === 0) {
    throw new Error('No data to export');
  }

  // Get headers from first object
  const headers = Object.keys(data[0]);
  
  // Create CSV content
  const csvContent = [
    headers.join(','), // Header row
    ...data.map(row => 
      headers.map(header => {
        const value = row[header];
        // Escape commas and quotes
        if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
          return `"${value.replace(/"/g, '""')}"`;
        }
        return value;
      }).join(',')
    )
  ].join('\n');

  // Create blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  downloadBlob(blob, filename);
};

/**
 * Export data as JSON
 */
export const exportToJSON = (data, filename = 'export.json') => {
  if (!data) {
    throw new Error('No data to export');
  }

  const jsonContent = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonContent], { type: 'application/json' });
  downloadBlob(blob, filename);
};

/**
 * Export data as PDF (basic text format)
 */
export const exportToPDF = (data, filename = 'export.pdf', title = 'Report') => {
  if (!data || data.length === 0) {
    throw new Error('No data to export');
  }

  // Create a simple text-based PDF content
  let pdfContent = `%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj

4 0 obj
<<
/Length 5 0 R
>>
stream
BT
/F1 12 Tf
50 750 Td
(${title}) Tj
0 -20 Td
(Generated: ${new Date().toLocaleString()}) Tj
0 -30 Td
`;

  // Add data rows
  data.forEach((row, index) => {
    if (index < 30) { // Limit to 30 rows for basic PDF
      const text = Object.entries(row)
        .map(([key, value]) => `${key}: ${value}`)
        .join(' | ');
      pdfContent += `(${text.substring(0, 80)}) Tj\n0 -15 Td\n`;
    }
  });

  pdfContent += `ET
endstream
endobj

5 0 obj
${pdfContent.split('stream')[1].split('endstream')[0].length}
endobj

xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000317 00000 n 
0000${String(pdfContent.length - 100).padStart(10, '0')} 00000 n 

trailer
<<
/Size 6
/Root 1 0 R
>>
startxref
${pdfContent.length}
%%EOF`;

  const blob = new Blob([pdfContent], { type: 'application/pdf' });
  downloadBlob(blob, filename);
};

/**
 * Helper function to download blob
 */
const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

/**
 * Format fraud log data for export
 */
export const formatFraudLogsForExport = (logs) => {
  return logs.map(log => ({
    'Timestamp': log.timestamp,
    'Phone Number': log.phone_number || 'N/A',
    'Risk Score': log.risk_score,
    'Risk Level': log.risk_level,
    'Threat Category': log.threat_category || 'Unknown',
    'Confidence': `${log.confidence}%`
  }));
};

/**
 * Format blacklist data for export
 */
export const formatBlacklistForExport = (blacklist) => {
  return blacklist.map(entry => ({
    'Phone Number': entry.phone_number,
    'Reason': entry.reason,
    'Added Date': entry.added_at
  }));
};

/**
 * Format analytics summary for export
 */
export const formatAnalyticsSummaryForExport = (summary) => {
  return [
    { 'Metric': 'Total Scans', 'Value': summary.total_scans || 0 },
    { 'Metric': 'High Risk', 'Value': summary.high_risk || 0 },
    { 'Metric': 'Medium Risk', 'Value': summary.medium_risk || 0 },
    { 'Metric': 'Low Risk', 'Value': summary.low_risk || 0 }
  ];
};
