import os

style_css_path = r"d:\company\antigravity\style.css"

extra_css = """

/* Report Selection Grid */
.report-selection-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.selection-card {
    background: white;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 30px 20px;
    text-align: center;
    cursor: pointer;
    transition: var(--transition);
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.selection-card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--accent-1);
    transform: translateY(-2px);
}

.selection-card .icon-wrapper {
    background: var(--bg-surface-hover);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
    color: var(--accent-2);
}

.selection-card .icon-wrapper i {
    width: 28px;
    height: 28px;
}

.selection-card h3 {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 5px;
}

.selection-card p {
    font-size: 14px;
    color: var(--text-secondary);
}

/* Form Shared Headers */
.form-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid var(--border-color);
}

.close-form-btn {
    border-radius: 100px;
}

/* Data Tables inside forms */
.table-responsive {
    overflow-x: auto;
    width: 100%;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

.data-table th, .data-table td {
    border: 1px solid var(--border-color);
    padding: 10px;
    text-align: center;
    font-size: 14px;
}

.data-table th {
    background: var(--bg-surface-hover);
    color: var(--text-secondary);
    font-weight: 600;
}

.data-table td input, .data-table td select {
    width: 100%;
    border: none;
    background: transparent;
    text-align: center;
    font-family: inherit;
    font-size: 14px;
    outline: none;
    color: var(--text-primary);
}

.data-table td input:focus, .data-table td select:focus {
    background: var(--bg-base);
    border-radius: 4px;
}

.data-table td input[type="number"] {
    -moz-appearance: textfield;
}

.input-group.grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
}

@media (max-width: 900px) {
    .input-group.grid-4 {
        grid-template-columns: 1fr 1fr;
    }
}
@media (max-width: 600px) {
    .input-group.grid-4 {
        grid-template-columns: 1fr;
    }
}
"""

with open(style_css_path, "a", encoding="utf-8") as f:
    f.write(extra_css)

print("Saved style.css")
