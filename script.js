/* =================================================
   JOBPILOT - APPLICATION SYSTEM
   ================================================= */


/* ================= SAMPLE JOBS ================= */

const jobs = [

    {
        id: 1,
        company: "TechNova Solutions",
        title: "Junior Data Analyst",
        location: "Chennai",
        salary: "₹25,000 - ₹40,000",
        skills: ["Python", "SQL", "Excel"]
    },

    {
        id: 2,
        company: "AI Vision Technologies",
        title: "AI/ML Intern",
        location: "Chennai",
        salary: "₹15,000 - ₹25,000",
        skills: ["Python", "Machine Learning", "SQL"]
    },

    {
        id: 3,
        company: "WebCore Systems",
        title: "Junior Python Developer",
        location: "Bangalore",
        salary: "₹30,000 - ₹45,000",
        skills: ["Python", "HTML", "JavaScript"]
    },

    {
        id: 4,
        company: "DataWorks",
        title: "Data Science Intern",
        location: "Remote",
        salary: "₹12,000 - ₹20,000",
        skills: ["Python", "SQL", "Machine Learning"]
    }

];


/* =================================================
   GET USER PROFILE
   ================================================= */

function getUser() {

    const user =
        localStorage.getItem("jobpilot_user");

    if (!user) {

        return null;

    }

    return JSON.parse(user);

}


/* =================================================
   SAVE USER PROFILE
   ================================================= */

function saveUser(user) {

    localStorage.setItem(
        "jobpilot_user",
        JSON.stringify(user)
    );

}


/* =================================================
   GET APPLICATIONS
   ================================================= */

function getApplications() {

    const applications =
        localStorage.getItem("jobpilot_applications");

    if (!applications) {

        return [];

    }

    return JSON.parse(applications);

}


/* =================================================
   SAVE APPLICATIONS
   ================================================= */

function saveApplications(applications) {

    localStorage.setItem(
        "jobpilot_applications",
        JSON.stringify(applications)
    );

}


/* =================================================
   APPROVE APPLICATION
   ================================================= */

function approveApplication(jobId) {

    const job =
        jobs.find(j => j.id == jobId);

    if (!job) {

        return;

    }


    const applications =
        getApplications();


    const existing =
        applications.find(
            app => app.jobId == jobId
        );


    if (existing) {

        alert(
            "Application already exists!"
        );

        return;

    }


    const newApplication = {

        id: Date.now(),

        jobId: job.id,

        company: job.company,

        title: job.title,

        location: job.location,

        salary: job.salary,

        status: "Approved",

        approvalStatus: "Approved",

        appliedDate:
            new Date().toLocaleDateString(),

        followUpDate: ""

    };


    applications.push(
        newApplication
    );


    saveApplications(
        applications
    );


    alert(
        "Application Approved Successfully! 🚀"
    );


    window.location.href =
        "application.html";

}


/* =================================================
   UPDATE APPLICATION STATUS
   ================================================= */

function updateApplicationStatus(
    applicationId,
    newStatus
) {

    const applications =
        getApplications();


    const application =
        applications.find(
            app => app.id == applicationId
        );


    if (!application) {

        return;

    }


    application.status =
        newStatus;


    saveApplications(
        applications
    );


    loadApplications();

}


/* =================================================
   SET FOLLOW-UP DATE
   ================================================= */

function setFollowUpDate(
    applicationId,
    date
) {

    const applications =
        getApplications();


    const application =
        applications.find(
            app => app.id == applicationId
        );


    if (!application) {

        return;

    }


    application.followUpDate =
        date;


    saveApplications(
        applications
    );

}


/* =================================================
   LOAD APPLICATIONS
   ================================================= */

function loadApplications() {

    const list =
        document.getElementById(
            "applicationList"
        );


    const empty =
        document.getElementById(
            "emptyState"
        );


    if (!list) {

        return;

    }


    const applications =
        getApplications();


    list.innerHTML = "";


    if (applications.length === 0) {

        empty.style.display =
            "block";

        return;

    }


    empty.style.display =
        "none";


    applications.forEach(
        application => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "application-card";


            card.innerHTML = `

                <h2>
                    ${application.title}
                </h2>

                <p>
                    🏢
                    <strong>
                        ${application.company}
                    </strong>
                </p>

                <p>
                    📍 ${application.location}
                </p>

                <p>
                    💰 ${application.salary}
                </p>

                <p>
                    📅 Applied:
                    ${application.appliedDate}
                </p>

                <p>
                    🤝 Approval:
                    <span class="status">
                        ${application.approvalStatus}
                    </span>
                </p>

                <p>
                    📌 Current Status:
                </p>

                <select
                    onchange="
                    updateApplicationStatus(
                        ${application.id},
                        this.value
                    )
                    "
                >

                    <option
                        ${application.status ===
                        "Approved" ? "selected" : ""}
                    >
                        Approved
                    </option>

                    <option
                        ${application.status ===
                        "Applied" ? "selected" : ""}
                    >
                        Applied
                    </option>

                    <option
                        ${application.status ===
                        "Interview" ? "selected" : ""}
                    >
                        Interview
                    </option>

                    <option
                        ${application.status ===
                        "Rejected" ? "selected" : ""}
                    >
                        Rejected
                    </option>

                    <option
                        ${application.status ===
                        "Selected" ? "selected" : ""}
                    >
                        Selected
                    </option>

                </select>


                <p>
                    🔔 Follow-up Date:
                </p>

                <input
                    type="date"
                    value="${application.followUpDate}"
                    onchange="
                    setFollowUpDate(
                        ${application.id},
                        this.value
                    )
                    "
                >

            `;


            list.appendChild(
                card
            );

        }
    );

}


/* =================================================
   PAGE LOAD
   ================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        loadApplications();

    }
);