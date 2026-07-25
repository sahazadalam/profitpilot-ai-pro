import { Card, CardContent } from "@/components/ui/Card";
import { motion } from "framer-motion";
import { TrendingUp, TrendingDown } from "lucide-react";

interface SalesCardProps {
  title: string;
  value: number;
  trend?: number;
}

export const SalesCard = ({ title, value, trend }: SalesCardProps) => {
  const isPositive = trend && trend > 0;

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      transition={{ duration: 0.2 }}
    >
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">{title}</p>
              <p className="text-2xl font-bold">${value}</p>
            </div>
            {trend && (
              <div className={"flex items-center gap-1 " + (isPositive ? "text-green-500" : "text-red-500")}>
                {isPositive ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                <span className="text-sm">{Math.abs(trend)}%</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};
