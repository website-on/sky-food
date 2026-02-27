import os

script_js_path = r"d:\company\antigravity\script.js"

content = """const firebaseConfig = {
    apiKey: "AIzaSyDzGC9Aic7CMkNfWp4WPVozumsXCQ0kccI",
    authDomain: "sky-food-8688f.firebaseapp.com",
    projectId: "sky-food-8688f",
    storageBucket: "sky-food-8688f.firebasestorage.app",
    messagingSenderId: "564779306186",
    appId: "1:564779306186:web:d841e4d8b607057c033833",
    measurementId: "G-ZM5402ZE1T"
};

if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}

const db = firebase.firestore();

let currentReports = [];

window.showForm = function(formId) {
    let sel = document.getElementById("reportSelection");
    if(sel) sel.classList.add("hidden");
    
    let f1 = document.getElementById("reportForm");
    let f2 = document.getElementById("dailyReportForm");
    if(f1) f1.classList.add("hidden");
    if(f2) f2.classList.add("hidden");
    
    let target = document.getElementById(formId);
    if(target) target.classList.remove("hidden");
    window.scrollTo({ top: 0, behavior: 'smooth' });
};

window.hideForms = function() {
    let f1 = document.getElementById("reportForm");
    let f2 = document.getElementById("dailyReportForm");
    if(f1) {
        f1.classList.add("hidden");
        f1.reset();
        f1.removeAttribute("data-edit-id");
    }
    if(f2) {
        f2.classList.add("hidden");
        f2.reset();
        f2.removeAttribute("data-edit-id");
    }
    
    let sel = document.getElementById("reportSelection");
    if(sel) sel.classList.remove("hidden");
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
};

document.addEventListener('DOMContentLoaded', () => {
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    const form = document.getElementById("reportForm");
    if (form) {
        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            const subBtn = form.querySelector(".submit-btn");
            const originalBtnHtml = subBtn.innerHTML;
            subBtn.innerHTML = "جاري الإرسال...";
            subBtn.disabled = true;

            let editId = form.getAttribute("data-edit-id");

            let report = {
                type: "annual",
                engineer: document.getElementById("engineer").value,
                area: document.getElementById("area").value,
                date: document.getElementById("date").value,
                opened: document.getElementById("opened").value || "0",
                damaged: document.getElementById("damaged").value || "0",
                good: document.getElementById("good").value || "0",
                prepared: document.getElementById("prepared").value || "0",
                used: document.getElementById("used").value || "0",
                concentration: document.getElementById("concentration").value || "0%",
                chloride: document.getElementById("chloride").value || "0",
                vinegar: document.getElementById("vinegar").value || "0",
                citric: document.getElementById("citric").value || "0",
                lactic: document.getElementById("lactic").value || "0",
                benzoate: document.getElementById("benzoate").value || "0",
                sulfur: document.getElementById("sulfur").value || "0",
                notes: document.getElementById("notes") ? document.getElementById("notes").value : "",
                timestamp: editId ? undefined : Date.now()
            };

            if (!editId) {
                report.managerSig = "";
                report.managerNotes = "";
            }

            try {
                if (editId) {
                    await db.collection('reports').doc(editId).update(report);
                    form.removeAttribute("data-edit-id");
                } else {
                    await db.collection('reports').add(report);
                }

                const successMessage = document.getElementById("successMessage");
                if (successMessage) {
                    successMessage.classList.remove("hidden");
                    setTimeout(() => { successMessage.classList.add("hidden"); }, 3000);
                }
                form.reset();
                window.hideForms();
            } catch (e) {
                console.error("Error writing document: ", e);
                alert("حدث خطأ أثناء حفظ التقرير.");
            } finally {
                subBtn.innerHTML = originalBtnHtml;
                subBtn.disabled = false;
            }
        });
    }

    const dailyForm = document.getElementById("dailyReportForm");
    if (dailyForm) {
        dailyForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const subBtn = dailyForm.querySelector(".submit-btn");
            const originalBtnHtml = subBtn.innerHTML;
            subBtn.innerHTML = "جاري الإرسال...";
            subBtn.disabled = true;

            let editId = dailyForm.getAttribute("data-edit-id");

            let report = {
                type: "daily",
                date: document.getElementById("daily_date").value,
                shift: document.getElementById("daily_shift").value,
                manager: document.getElementById("daily_manager").value,
                
                t_sol_count: document.getElementById("t_sol_count").value || "0",
                t_sol_full: document.getElementById("t_sol_full").value || "0",
                t_sol_half: document.getElementById("t_sol_half").value || "0",
                t_sol_low: document.getElementById("t_sol_low").value || "0",
                t_sol_empty: document.getElementById("t_sol_empty").value || "0",
                t_sol_total: document.getElementById("t_sol_total").value || "0",
                
                t_wat_count: document.getElementById("t_wat_count").value || "0",
                t_wat_full: document.getElementById("t_wat_full").value || "0",
                t_wat_half: document.getElementById("t_wat_half").value || "0",
                t_wat_low: document.getElementById("t_wat_low").value || "0",
                t_wat_empty: document.getElementById("t_wat_empty").value || "0",
                t_wat_total: document.getElementById("t_wat_total").value || "0",
                
                t_sod_count: document.getElementById("t_sod_count").value || "0",
                t_sod_full: document.getElementById("t_sod_full").value || "0",
                t_sod_half: document.getElementById("t_sod_half").value || "0",
                t_sod_low: document.getElementById("t_sod_low").value || "0",
                t_sod_empty: document.getElementById("t_sod_empty").value || "0",
                t_sod_total: document.getElementById("t_sod_total").value || "0",

                fu_section: document.getElementById("fu_section").value || "",
                fu_tank_no: document.getElementById("fu_tank_no").value || "",
                fu_status: document.getElementById("fu_status").value || "",
                fu_action: document.getElementById("fu_action").value || "",

                s_chlor_current: document.getElementById("s_chlor_current").value || "0",
                s_chlor_min: document.getElementById("s_chlor_min").value || "0",
                s_chlor_order: document.getElementById("s_chlor_order").value || "لا",
                s_lac_current: document.getElementById("s_lac_current").value || "0",
                s_lac_min: document.getElementById("s_lac_min").value || "0",
                s_lac_order: document.getElementById("s_lac_order").value || "لا",
                s_cit_current: document.getElementById("s_cit_current").value || "0",
                s_cit_min: document.getElementById("s_cit_min").value || "0",
                s_cit_order: document.getElementById("s_cit_order").value || "لا",
                s_vin_current: document.getElementById("s_vin_current").value || "0",
                s_vin_min: document.getElementById("s_vin_min").value || "0",
                s_vin_order: document.getElementById("s_vin_order").value || "لا",
                s_sul_current: document.getElementById("s_sul_current").value || "0",
                s_sul_min: document.getElementById("s_sul_min").value || "0",
                s_sul_order: document.getElementById("s_sul_order").value || "لا",
                s_ben_current: document.getElementById("s_ben_current").value || "0",
                s_ben_min: document.getElementById("s_ben_min").value || "0",
                s_ben_order: document.getElementById("s_ben_order").value || "لا",
                s_salt_current: document.getElementById("s_salt_current").value || "0",
                s_salt_min: document.getElementById("s_salt_min").value || "0",
                s_salt_order: document.getElementById("s_salt_order").value || "لا",

                notes: document.getElementById("daily_notes").value || "",
                timestamp: editId ? undefined : Date.now()
            };

            if (!editId) {
                report.managerSig = "";
                report.managerNotes = "";
            }

            try {
                if (editId) {
                    await db.collection('reports').doc(editId).update(report);
                    dailyForm.removeAttribute("data-edit-id");
                } else {
                    await db.collection('reports').add(report);
                }

                const successMessage = document.getElementById("successMessage");
                if (successMessage) {
                    successMessage.classList.remove("hidden");
                    setTimeout(() => { successMessage.classList.add("hidden"); }, 3000);
                }
                dailyForm.reset();
                window.hideForms();
            } catch (e) {
                console.error("Error writing document: ", e);
                alert("حدث خطأ أثناء حفظ التقرير.");
            } finally {
                subBtn.innerHTML = originalBtnHtml;
                subBtn.disabled = false;
            }
        });
    }

});

window.deleteReport = async function (id) {
    if (confirm("هل تريد بالتأكيد حذف هذا التقرير؟")) {
        try {
            await db.collection('reports').doc(id).delete();
            if (document.getElementById("reportsList")) {
                await window.loadReports();
            }
        } catch (e) {
            console.error("Error deleting document: ", e);
            alert("حدث خطأ في حذف التقرير.");
        }
    }
};

window.saveAdminData = async function (id) {
    try {
        let sig = document.getElementById("sig_" + id).value;
        let mnotes = document.getElementById("mnotes_" + id).value;

        await db.collection('reports').doc(id).update({
            managerSig: sig,
            managerNotes: mnotes
        });

        alert("تم حفظ اعتماد المسؤول بنجاح!");
        await window.loadReports();
    } catch (e) {
        console.error("Error updating admin data", e);
        alert("حدث خطأ أثناء الحفظ.");
    }
}

window.checkPassword = function () {
    let pass = document.getElementById("adminPass").value;
    if (pass === "1357") {
        document.getElementById("reportsContainer").classList.remove("hidden");
        const floatingAdmin = document.querySelector(".admin-floating");
        if (floatingAdmin) floatingAdmin.classList.add("hidden");
        window.loadReports();
    } else {
        alert("الرقم السري غير صحيح. حاول مرة أخرى.");
    }
};

window.loadReports = async function () {
    let container = document.getElementById("reportsList");
    if (!container) return;

    container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 40px;">
            <p>جاري تحميل البيانات...</p>
        </div>
    `;

    try {
        const querySnapshot = await db.collection('reports').get();
        currentReports = [];
        querySnapshot.forEach((doc) => {
            currentReports.push({ id: doc.id, ...doc.data() });
        });

        currentReports.sort((a, b) => (b.timestamp || Number(new Date(b.date))) - (a.timestamp || Number(new Date(a.date))));

        container.innerHTML = "";

        if (currentReports.length === 0) {
            container.innerHTML = `
                <div style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 40px;">
                    <i data-lucide="inbox" style="width: 48px; height: 48px; opacity: 0.5;"></i>
                    <p>لا توجد تقارير في قاعدة البيانات.</p>
                </div>
            `;
            if (typeof lucide !== 'undefined') lucide.createIcons();
            return;
        }

        currentReports.forEach(r => {
            const dateObj = new Date(r.date);
            const dateStr = !isNaN(dateObj) ? dateObj.toLocaleDateString('ar-EG', { year: 'numeric', month: 'long', day: 'numeric' }) : r.date;
            
            let cardHtml = "";

            if(r.type === "daily") {
                let requests = [
                    r.s_chlor_order === "نعم" ? "كلوريد" : "",
                    r.s_lac_order === "نعم" ? "لاكتيك" : "",
                    r.s_cit_order === "نعم" ? "ستريك" : "",
                    r.s_vin_order === "نعم" ? "خل" : "",
                    r.s_sul_order === "نعم" ? "كبريت" : "",
                    r.s_ben_order === "نعم" ? "بنزوات" : "",
                    r.s_salt_order === "نعم" ? "ملح" : ""
                ].filter(Boolean).join(" | ");

                cardHtml = `
                    <div class="report-card">
                        <div class="rc-header">
                            <span class="rc-title"><i data-lucide="sun" style="width:18px; margin-left:6px; color:var(--accent-1);"></i> التقرير اليومي – وحدة المحاليل</span>
                            <span class="rc-date">${dateStr}</span>
                        </div>
                        <div class="rc-body">
                            <p><span class="rc-label">الوردية:</span> <span class="rc-value">${r.shift}</span></p>
                            <p><span class="rc-label">مسؤول التخزين:</span> <span class="rc-value danger-text">${r.managerSig || r.manager}</span></p>
                            
                            <div class="rc-box">
                                <span class="rc-label" style="display:block; margin-bottom:8px; border-bottom:1px solid #cbd5e1; padding-bottom:4px;">توزيع حالة التنكات:</span>
                                <table style="width:100%; font-size:13px; text-align:center; border-collapse:collapse; margin-bottom:10px;">
                                    <tr style="background:#f1f5f9;"><th>النوع</th><th>العدد</th><th>ممتلئ</th><th>نصف</th><th>منخفض</th><th>فارغ</th><th>الكمية(طن)</th></tr>
                                    <tr style="border-bottom:1px solid #e2e8f0;"><td>المحلول</td><td>${r.t_sol_count}</td><td>${r.t_sol_full}</td><td>${r.t_sol_half}</td><td>${r.t_sol_low}</td><td>${r.t_sol_empty}</td><td>${r.t_sol_total}</td></tr>
                                    <tr style="border-bottom:1px solid #e2e8f0;"><td>المياه</td><td>${r.t_wat_count}</td><td>${r.t_wat_full}</td><td>${r.t_wat_half}</td><td>${r.t_wat_low}</td><td>${r.t_wat_empty}</td><td>${r.t_wat_total}</td></tr>
                                    <tr><td>الصودا</td><td>${r.t_sod_count}</td><td>${r.t_sod_full}</td><td>${r.t_sod_half}</td><td>${r.t_sod_low}</td><td>${r.t_sod_empty}</td><td>${r.t_sod_total}</td></tr>
                                </table>
                            </div>

                            <div class="rc-box">
                                <span class="rc-label">متابعة التنكات:</span><br>
                                القسم: ${r.fu_section} | تنك: ${r.fu_tank_no} | حالة: ${r.fu_status} | الإجراء: ${r.fu_action}
                            </div>

                            <div class="rc-box" style="background:#fef2f2; border:1px solid #fca5a5;">
                                <span class="rc-label" style="color:#b91c1c;">طلبات توريد عاجلة (نعم):</span><br>
                                <strong style="color:#7f1d1d;">${requests || "لا توجد طلبات"}</strong>
                            </div>
                        </div>
                        
                         <div class="rc-alerts admin-panel">
                            <h4><i data-lucide="shield-check"></i> لوحة تحكم المسؤول</h4>
                            <div class="admin-inputs" style="margin-top:16px; display:flex; flex-direction:column; gap:12px;">
                                <div class="input-field">
                                    <label style="font-size:13px; color:#991b1b; font-weight:700;">توقيع المسؤول على التقرير</label>
                                    <input type="text" id="sig_${r.id}" value="${r.managerSig || ''}" placeholder="اسم وتوقيع المسؤول (سيظهر في أعلى التقرير لاحقاً)" style="border:1px solid #fca5a5; background:#fff; padding:8px;">
                                </div>
                                <div class="input-field">
                                    <label style="font-size:13px; color:#991b1b; font-weight:700;">ملاحظات المسؤول</label>
                                    <textarea id="mnotes_${r.id}" placeholder="اكتب ملاحظات المسؤول هنا..." rows="2" style="border:1px solid #fca5a5; background:#fff; padding:8px;">${r.managerNotes || ''}</textarea>
                                </div>
                                <button onclick="window.saveAdminData('${r.id}')" class="btn" style="background:#b91c1c; color:white; align-self:flex-start; outline:none; border:none; padding:8px 20px; border-radius:6px; cursor:pointer;"><i data-lucide="check-circle" style="width:16px;height:16px;"></i> حفظ الاعتماد</button>
                            </div>

                            <div class="alert-notes" style="margin-top:16px;">
                                <span class="alert-label">ملاحظات عامة من المنشئ:</span>
                                <p>${r.notes || "لا توجد ملاحظات."}</p>
                            </div>
                        </div>

                         <div class="rc-footer justify-end" style="border-top:none; margin-top:0;">
                            <button onclick="window.deleteReport('${r.id}')" class="btn btn-danger" style="margin-right:auto;"><i data-lucide="trash-2"></i> حذف (أدمن)</button>
                        </div>
                    </div>
                `;
            } else {
                // Annual (old format)
                let openedNum = parseInt(r.opened) || 0;
                let damagedNum = parseInt(r.damaged) || 0;
                let damageRate = openedNum > 0 ? ((damagedNum / openedNum) * 100).toFixed(2) : "0.00";

                cardHtml = `
                    <div class="report-card">
                        <div class="rc-header">
                            <span class="rc-title"><i data-lucide="calendar" style="width:18px; margin-left:6px; color:var(--accent-2);"></i> التقرير السنوي – ${r.engineer || "غير محدد"}</span>
                            <span class="rc-date">${dateStr}</span>
                        </div>
                        <div class="rc-body">
                            <p><span class="rc-label">المنطقة:</span> <span class="rc-value">${r.area}</span></p>
                            <p><span class="rc-label">البراميل:</span> <span class="rc-value">مفتوحة ${r.opened} - مخرومة <span class="danger-text">${r.damaged}</span> - سليمة ${r.good}</span></p>
                            <p><span class="rc-label">المحلول:</span> <span class="rc-value">مجهز ${r.prepared} - مستخدم ${r.used} طن - تركيز ${r.concentration}</span></p>
                            <div class="rc-box">
                                <span class="rc-label">المستلزمات:</span>
                                كلوريد ${r.chloride} | خل ${r.vinegar} | ستريك ${r.citric} | لاكتيك ${r.lactic} | بنزوات ${r.benzoate} | كبريت ${r.sulfur}
                            </div>
                        </div>
                        
                         <div class="rc-alerts admin-panel">
                            <h4><i data-lucide="shield-check"></i> لوحة تحكم المسؤول</h4>
                            <div class="alert-grid" style="grid-template-columns: 1fr;">
                                <div class="alert-item">
                                    <span class="alert-label">نسبة التلف بالمنطقة</span>
                                    <span class="alert-value danger-text">${damageRate}%</span>
                                </div>
                            </div>
                            
                            <div class="admin-inputs" style="margin-top:16px; display:flex; flex-direction:column; gap:12px;">
                                <div class="input-field">
                                    <label style="font-size:13px; color:#991b1b; font-weight:700;">توقيع المسؤول</label>
                                    <input type="text" id="sig_${r.id}" value="${r.managerSig || ''}" placeholder="اسم وتوقيع المسؤول" style="border:1px solid #fca5a5; background:#fff; padding:8px;">
                                </div>
                                <div class="input-field">
                                    <label style="font-size:13px; color:#991b1b; font-weight:700;">ملاحظات المسؤول</label>
                                    <textarea id="mnotes_${r.id}" placeholder="اكتب ملاحظات المسؤول هنا..." rows="2" style="border:1px solid #fca5a5; background:#fff; padding:8px;">${r.managerNotes || ''}</textarea>
                                </div>
                                <button onclick="window.saveAdminData('${r.id}')" class="btn" style="background:#b91c1c; color:white; align-self:flex-start; outline:none; border:none; padding:8px 20px; border-radius:6px; cursor:pointer;"><i data-lucide="check-circle" style="width:16px;height:16px;"></i> حفظ الاعتماد</button>
                            </div>

                            <div class="alert-notes" style="margin-top:16px;">
                                <span class="alert-label">ملاحظات المهندس:</span>
                                <p>${r.notes || "لا توجد ملاحظات."}</p>
                            </div>
                        </div>

                         <div class="rc-footer justify-end" style="border-top:none; margin-top:0;">
                            <button onclick="window.deleteReport('${r.id}')" class="btn btn-danger" style="margin-right:auto;"><i data-lucide="trash-2"></i> حذف (أدمن)</button>
                        </div>
                    </div>
                `;
            }

            container.innerHTML += cardHtml;
        });

        if (typeof lucide !== 'undefined') lucide.createIcons();

    } catch (e) {
        console.error("Error fetching documents: ", e);
        container.innerHTML = `<p style="color:red; text-align:center;">حدث خطأ في تحميل البيانات من الخادم.</p>`;
    }
};
"""

with open(script_js_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Saved script.js")
