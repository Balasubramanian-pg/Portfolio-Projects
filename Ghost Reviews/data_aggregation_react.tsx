import { 
  Target, 
  Database, 
  FileText, 
  AlertTriangle, 
  Settings, 
  CheckCircle, 
  BarChart3,
  Download,
  RefreshCw,
  Shield,
  Clock,
  HardDrive,
  Package
} from "lucide-react";

export default function DataAggregationStrategy() {
  return (
    <div className="max-w-4xl mx-auto p-8 bg-gradient-to-br from-slate-50 to-blue-50 min-h-screen">
      <div className="bg-white rounded-xl shadow-lg p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Phase 1: Data Aggregation & Cleaning Strategy
          </h1>
          <div className="w-24 h-1 bg-blue-500 mx-auto rounded"></div>
        </div>

        {/* Objective */}
        <div className="mb-8 p-6 bg-blue-50 rounded-lg border-l-4 border-blue-500">
          <div className="flex items-center mb-3">
            <Target className="text-blue-600 mr-3" size={24} />
            <h2 className="text-xl font-semibold text-gray-800">Objective</h2>
          </div>
          <p className="text-gray-700">
            Integrate and clean fragmented customer data from multiple sources to create a unified, 
            high-quality dataset for churn prediction modeling.
          </p>
        </div>

        {/* Data Sources */}
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <Database className="text-green-600 mr-3" size={24} />
            <h2 className="text-xl font-semibold text-gray-800">Data Sources Overview</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-50 p-4 rounded-lg border">
              <h3 className="font-semibold text-gray-800 mb-2">CRM Database</h3>
              <p className="text-sm text-gray-600 mb-1">Format: SQL</p>
              <p className="text-sm text-gray-600 mb-1">Volume: ~500K records</p>
              <p className="text-sm text-gray-600">Customer profiles, plans, tenure</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg border">
              <h3 className="font-semibold text-gray-800 mb-2">Usage Logs</h3>
              <p className="text-sm text-gray-600 mb-1">Format: CSV</p>
              <p className="text-sm text-gray-600 mb-1">Volume: ~2M+ rows</p>
              <p className="text-sm text-gray-600">Activity metrics, consumption</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg border">
              <h3 className="font-semibold text-gray-800 mb-2">Support Tickets</h3>
              <p className="text-sm text-gray-600 mb-1">Format: JSON</p>
              <p className="text-sm text-gray-600 mb-1">Volume: ~100K entries</p>
              <p className="text-sm text-gray-600">Sentiment, resolution times</p>
            </div>
          </div>
        </div>

        {/* Critical Challenges */}
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <AlertTriangle className="text-red-600 mr-3" size={24} />
            <h2 className="text-xl font-semibold text-gray-800">Critical Challenges</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-400">
              <h3 className="font-semibold text-gray-800 mb-2">Data Quality Issues</h3>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• 15% missing values in Upgrade_History</li>
                <li>• Negative tenure values requiring correction</li>
                <li>• Inconsistent date formats across sources</li>
              </ul>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg border-l-4 border-orange-400">
              <h3 className="font-semibold text-gray-800 mb-2">Technical Constraints</h3>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• 2M+ row performance optimization</li>
                <li>• Multi-format integration (SQL → CSV → JSON)</li>
                <li>• Memory-efficient processing requirements</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Implementation Workflow */}
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <Settings className="text-purple-600 mr-3" size={24} />
            <h2 className="text-xl font-semibold text-gray-800">Implementation Workflow</h2>
          </div>
          
          <div className="space-y-6">
            {/* Extract & Load */}
            <div className="border-l-4 border-green-400 pl-6">
              <div className="flex items-center mb-2">
                <Download className="text-green-600 mr-2" size={20} />
                <h3 className="font-semibold text-gray-800">Extract & Load</h3>
              </div>
              <div className="bg-gray-100 p-4 rounded-lg">
                <pre className="text-sm overflow-x-auto">
{`-- CRM Data Extraction
SELECT Customer_ID, Plan_Type, Tenure, Monthly_Charges, Upgrade_History  
FROM customers WHERE Status = 'Active';

# Load supplementary data
usage_data = pd.read_csv("usage_logs.csv", chunksize=50000)
support_data = pd.read_json("support_tickets.json", lines=True)`}
                </pre>
              </div>
            </div>

            {/* Clean & Transform */}
            <div className="border-l-4 border-blue-400 pl-6">
              <div className="flex items-center mb-2">
                <RefreshCw className="text-blue-600 mr-2" size={20} />
                <h3 className="font-semibold text-gray-800">Clean & Transform</h3>
              </div>
              <div className="bg-gray-100 p-4 rounded-lg">
                <pre className="text-sm overflow-x-auto">
{`# Fix data inconsistencies
data['Tenure'] = data['Tenure'].abs()  # Remove negative values
data['Upgrade_History'].fillna("No_Upgrade", inplace=True)

# Sentiment scoring
sentiment_map = {'frustrated': -1, 'neutral': 0, 'satisfied': 1}
support_data['Sentiment_Score'] = support_data['Sentiment_Text'].map(sentiment_map)`}
                </pre>
              </div>
            </div>

            {/* Integrate & Validate */}
            <div className="border-l-4 border-orange-400 pl-6">
              <div className="flex items-center mb-2">
                <Shield className="text-orange-600 mr-2" size={20} />
                <h3 className="font-semibold text-gray-800">Integrate & Validate</h3>
              </div>
              <div className="bg-gray-100 p-4 rounded-lg">
                <pre className="text-sm overflow-x-auto">
{`# Sequential merge with validation
final_dataset = (usage_data
                 .merge(support_data, on="Customer_ID", how="left")
                 .merge(crm_data, on="Customer_ID", how="inner"))

# Quality assurance
completeness_rate = (1 - final_dataset.isnull().sum() / len(final_dataset)) * 100
assert completeness_rate.min() > 95, "Data completeness below threshold"`}
                </pre>
              </div>
            </div>
          </div>
        </div>

        {/* Success Metrics */}
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <BarChart3 className="text-indigo-600 mr-3" size={24} />
            <h2 className="text-xl font-semibold text-gray-800">Success Metrics</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-green-50 p-4 rounded-lg text-center border">
              <CheckCircle className="text-green-600 mx-auto mb-2" size={32} />
              <h3 className="font-semibold text-gray-800">Data Completeness</h3>
              <p className="text-2xl font-bold text-green-600">&gt;95%</p>
              <p className="text-sm text-gray-600">Model reliability</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg text-center border">
              <Clock className="text-blue-600 mx-auto mb-2" size={32} />
              <h3 className="font-semibold text-gray-800">Processing Time</h3>
              <p className="text-2xl font-bold text-blue-600">&lt;30 min</p>
              <p className="text-sm text-gray-600">Operational efficiency</p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg text-center border">
              <HardDrive className="text-purple-600 mx-auto mb-2" size={32} />
              <h3 className="font-semibold text-gray-800">Memory Usage</h3>
              <p className="text-2xl font-bold text-purple-600">&lt;8GB</p>
              <p className="text-sm text-gray-600">Resource optimization</p>
            </div>
          </div>
        </div>

        {/* Deliverables */}
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <Package className="text-teal-600 mr-3" size={24} />
            <h2 className="text-xl font-semibold text-gray-800">Deliverables</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center p-3 bg-green-50 rounded-lg border-l-4 border-green-400">
              <CheckCircle className="text-green-600 mr-3" size={20} />
              <div>
                <h3 className="font-semibold text-gray-800">Unified Dataset</h3>
                <p className="text-sm text-gray-600">Single source of truth with standardized schema</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-green-50 rounded-lg border-l-4 border-green-400">
              <CheckCircle className="text-green-600 mr-3" size={20} />
              <div>
                <h3 className="font-semibold text-gray-800">Data Dictionary</h3>
                <p className="text-sm text-gray-600">Complete field mappings and transformation rules</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-green-50 rounded-lg border-l-4 border-green-400">
              <CheckCircle className="text-green-600 mr-3" size={20} />
              <div>
                <h3 className="font-semibold text-gray-800">Quality Report</h3>
                <p className="text-sm text-gray-600">Validation results and processing metrics</p>
              </div>
            </div>
            <div className="flex items-center p-3 bg-green-50 rounded-lg border-l-4 border-green-400">
              <CheckCircle className="text-green-600 mr-3" size={20} />
              <div>
                <h3 className="font-semibold text-gray-800">Processing Pipeline</h3>
                <p className="text-sm text-gray-600">Reusable scripts for future data updates</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white">
          <p className="font-semibold">Ready for Phase 2: Feature Engineering & Model Development</p>
        </div>
      </div>
    </div>
  );
}