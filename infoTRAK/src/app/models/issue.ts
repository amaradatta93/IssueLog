export class Issue {
    id: number;
    customer_name: string;
    company: string;
    source: string;
    email: string;
    phone: string;
    issue_report_date: string;
    issue_description: string;
    domain: string;
    priority: string;
    assigned_to: string;
    issue_fix_date: string;
    status: string;
    support_engineer_comments: string;
    issue_file: string;
}

export class DashboardIssues {
    id: number;
    company: string;
    issue_report_date: string;
    issue_description: string;
    priority: string;
    domain: string;
    assigned_to: string;
    status: string;
}
