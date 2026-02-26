const firebaseConfig = {
    apiKey: "AIzaSyDzGC9Aic7CMkNfWp4WPVozumsXCQ0kccI",
    authDomain: "sky-food-8688f.firebaseapp.com",
    projectId: "sky-food-8688f",
    storageBucket: "sky-food-8688f.firebasestorage.app",
    messagingSenderId: "564779306186",
    appId: "1:564779306186:web:d841e4d8b607057c033833",
    measurementId: "G-ZM5402ZE1T"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// Global Reports Array to keep UI sync fast
let currentReports = [];

document.addEventListener('DOMContentLoaded', () => {
    // Initialize premium icons safely
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    const openBtn = document.getElementById("openFormBtn");
    if (openBtn) {
        openBtn.onclick = function () {
            document.getElementById("reportForm").classList.remove("hidden");
            openBtn.style.display = "none";
        };

        const cancelBtn = document.getElementById('cancelBtn');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                document.getElementById('reportForm').classList.add('hidden');
                openBtn.style.display = 'inline-flex';
                document.getElementById('reportForm').reset();
                document.getElementById("reportForm").removeAttribute("data-edit-id");
            });
        }
    }

    const form = document.getElementById("reportForm");
    if (form) {
        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            // UX state: Disable button temporarily while sending
            const subBtn = document.querySelector(".submit-btn");
            const originalBtnHtml = subBtn.innerHTML;
            subBtn.innerHTML = "جاري الإرسال...";
            subBtn.disabled = true;

            let editId = form.getAttribute("data-edit-id");

            let report = {
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
                timestamp: editId ? undefined : Date.now() // For sorting safely
            };

            // New reports start without manager approval
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
                form.classList.add("hidden");
                if (openBtn) openBtn.style.display = "inline-flex";

            } catch (e) {
                console.error("Error writing document: ", e);
                alert("حدث خطأ أثناء حفظ التقرير. يرجى المحاولة مرة أخرى.");
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

window.editReport = function (id) {
    let r = currentReports.find(report => report.id === id);
    if (!r) return;

    document.getElementById("engineer").value = r.engineer || "";
    document.getElementById("area").value = r.area || "";
    document.getElementById("date").value = r.date || "";
    document.getElementById("opened").value = r.opened || "";
    document.getElementById("damaged").value = r.damaged || "";
    document.getElementById("good").value = r.good || "";
    document.getElementById("prepared").value = r.prepared || "";
    document.getElementById("used").value = r.used || "";
    document.getElementById("concentration").value = r.concentration || "";
    document.getElementById("chloride").value = r.chloride || "";
    document.getElementById("vinegar").value = r.vinegar || "";
    document.getElementById("citric").value = r.citric || "";
    document.getElementById("lactic").value = r.lactic || "";
    document.getElementById("benzoate").value = r.benzoate || "";
    document.getElementById("sulfur").value = r.sulfur || "";

    if (document.getElementById("notes")) document.getElementById("notes").value = r.notes || "";

    const form = document.getElementById("reportForm");
    const openBtn = document.getElementById("openFormBtn");

    if (form) form.classList.remove("hidden");
    if (openBtn) openBtn.style.display = "none";

    if (form) form.scrollIntoView({ behavior: 'smooth' });
    if (form) form.setAttribute("data-edit-id", id);
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
        <div style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 40px; background: var(--bg-surface-hover); border-radius: 16px;">
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
                <div style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 40px; background: var(--bg-surface-hover); border-radius: 16px;">
                    <i data-lucide="inbox" style="width: 48px; height: 48px; opacity: 0.5; margin-bottom: 16px;"></i>
                    <p>لا توجد تقارير في قاعدة البيانات.</p>
                </div>
            `;
            if (typeof lucide !== 'undefined') lucide.createIcons();
            return;
        }

        currentReports.forEach(r => {
            const dateObj = new Date(r.date);
            const dateStr = !isNaN(dateObj) ? dateObj.toLocaleDateString('ar-EG', { year: 'numeric', month: 'long', day: 'numeric' }) : r.date;

            let openedNum = parseInt(r.opened) || 0;
            let damagedNum = parseInt(r.damaged) || 0;
            let damageRate = openedNum > 0 ? ((damagedNum / openedNum) * 100).toFixed(2) : "0.00";

            container.innerHTML += `
            <div class="report-card">
                <div class="rc-header">
                    <span class="rc-title"><i data-lucide="user" style="width:16px; height:16px; display:inline-block; vertical-align:middle; margin-left:4px;"></i> ${r.engineer}</span>
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
        });
        if (typeof lucide !== 'undefined') lucide.createIcons();

    } catch (e) {
        console.error("Error fetching documents: ", e);
        container.innerHTML = `<p style="color:red; text-align:center;">حدث خطأ في تحميل البيانات من الخادم.</p>`;
    }
};
