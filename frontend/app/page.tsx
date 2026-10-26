'use client';

import { ChangeEvent, useMemo, useState } from 'react';

const CATEGORY_OPTIONS = [
  'Software & Subscriptions',
  'Travel & Transport',
  'Meals & Dining',
  'Office & Supplies',
  'Groceries',
  'Health & Wellness',
  'Housing & Utilities',
  'Income & Transfers',
  'Refund / Reimbursement',
  'Needs Review',
];

type Row = {
  description: string;
  amount: number;
  category: string;
  needs_review: boolean;
  confidence: string;
};

type Summary = {
  category_totals: Record<string, number>;
  review_count: number;
  spend_total: number;
  transaction_count: number;
};

export default function Page() {
  const [rows, setRows] = useState<Row[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8002';

    try {
      const response = await fetch(`${apiUrl}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setRows(data.rows ?? []);
      setSummary(data.summary ?? null);
    } catch (error) {
      console.error(error);
      setRows([]);
      setSummary(null);
      alert('Unable to upload that statement. Please check the CSV format and try again.');
    } finally {
      setLoading(false);
      event.target.value = '';
    }
  };

  const handleCategoryChange = (index: number, updatedCategory: string) => {
    setRows((current) => current.map((row, rowIndex) => rowIndex === index ? { ...row, category: updatedCategory, needs_review: updatedCategory === 'Needs Review' } : row));
    setSummary((current) => {
      if (!current) return current;
      const nextTotals = { ...current.category_totals };
      const original = rows[index];
      if (!original) return current;
      nextTotals[original.category] = (nextTotals[original.category] || 0) - original.amount;
      nextTotals[updatedCategory] = (nextTotals[updatedCategory] || 0) + original.amount;
      if (original.category === 'Needs Review') {
        current.review_count = Math.max(0, current.review_count - 1);
      }
      if (updatedCategory === 'Needs Review') {
        current.review_count += 1;
      }
      return { ...current, category_totals: nextTotals };
    });
  };

  const totalForCategory = useMemo(() => {
    return rows.reduce<Record<string, number>>((acc, row) => {
      acc[row.category] = (acc[row.category] || 0) + row.amount;
      return acc;
    }, {});
  }, [rows]);

  return (
    <main className="container">
      <header className="header">
        <h1>Statement Categorizer</h1>
        <p>Sort credit-card and bank transactions for tax time with a transparent, rules-based review flow.</p>
      </header>

      <section className="card">
        <div className="toolbar">
          <label className="upload-input">
            <input type="file" accept=".csv" onChange={handleUpload} />
          </label>
          <button type="button" disabled={loading}>{loading ? 'Processing…' : 'Upload statement'}</button>
        </div>

        {summary && (
          <div className="summary-grid">
            <div className="summary-box">
              <h3>Spend total</h3>
              <strong>${Math.abs(summary.spend_total).toFixed(2)}</strong>
            </div>
            <div className="summary-box">
              <h3>Transactions</h3>
              <strong>{summary.transaction_count}</strong>
            </div>
            <div className="summary-box">
              <h3>Needs review</h3>
              <strong>{summary.review_count}</strong>
            </div>
          </div>
        )}
      </section>

      {rows.length > 0 && (
        <section className="card" style={{ marginTop: 24 }}>
          <h2>Review results</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Description</th>
                  <th>Amount</th>
                  <th>Category</th>
                  <th>Confidence</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row, index) => (
                  <tr key={`${row.description}-${index}`}>
                    <td>{row.description}</td>
                    <td>{row.amount.toFixed(2)}</td>
                    <td>
                      <span className={`tag ${row.needs_review ? 'review' : ''}`}>{row.category}</span>
                    </td>
                    <td>{row.confidence}</td>
                    <td>
                      <select
                        value={row.category}
                        onChange={(event) => handleCategoryChange(index, event.target.value)}
                      >
                        {CATEGORY_OPTIONS.map((category) => (
                          <option key={category} value={category}>{category}</option>
                        ))}
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="note">
            Total by category: {Object.entries(totalForCategory).map(([category, value]) => `${category}: $${Math.abs(value).toFixed(2)}`).join(' • ')}
          </div>
        </section>
      )}
    </main>
  );
}
