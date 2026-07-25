import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { motion } from "framer-motion";
import { Activity } from "lucide-react";

interface BusinessHealthProps {
  score: number;
}

export const BusinessHealth = ({ score }: BusinessHealthProps) => {
  const getStatus = (score: number) => {
    if (score >= 80) return { label: "Excellent", color: "text-green-500" };
    if (score >= 60) return { label: "Good", color: "text-yellow-500" };
    if (score >= 40) return { label: "Average", color: "text-orange-500" };
    return { label: "Critical", color: "text-red-500" };
  };

  const status = getStatus(score);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="h-5 w-5" />
            Business Health
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center">
            <div className="text-5xl font-bold">{score}</div>
            <div className={"text-lg font-medium " + status.color}>{status.label}</div>
            <div className="mt-4 h-2 w-full rounded-full bg-secondary">
              <div
                className="h-2 rounded-full bg-gradient-to-r from-red-500 via-yellow-500 to-green-500"
                style={{ width: score + "%" }}
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};

