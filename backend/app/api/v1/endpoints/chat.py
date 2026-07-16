"""
Chat endpoints for AI Business Assistant.
"""
from fastapi import APIRouter, Depends, status, Query
from typing import Optional

from app.services.chat_service import chat_service
from app.dependencies.auth import get_current_active_user
from app.schemas.auth import UserResponse
from app.core.exceptions import AppException

import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Send a message to AI Business Assistant",
    description="Get AI-powered business answers and recommendations"
)
async def send_message(
    request: dict,
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Send a message to the AI Business Assistant.
    """
    try:
        question = request.get("question", "")
        conversation_id = request.get("conversation_id")
        
        if not question:
            return {
                "success": False,
                "message": "Question is required",
                "data": None
            }
        
        result = await chat_service.process_chat(
            user_id=current_user.id,
            question=question,
            conversation_id=conversation_id
        )
        
        return {
            "success": True,
            "message": "Business assistant response generated",
            "data": result
        }
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        raise AppException(
            message=f"Failed to process chat: {str(e)}",
            status_code=500,
            error_code="CHAT_PROCESSING_FAILED"
        )


@router.post(
    "/query",
    status_code=status.HTTP_200_OK,
    summary="Send a query (alias for /chat)",
    description="Alias endpoint for sending queries to AI Business Assistant"
)
async def send_query(
    request: dict,
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Send a query to the AI Business Assistant.
    """
    return await send_message(request, current_user)


@router.get(
    "/history",
    status_code=status.HTTP_200_OK,
    summary="Get chat history",
    description="Get conversation history by conversation ID"
)
async def get_history(
    conversation_id: str = Query(..., description="Conversation ID"),
    limit: int = Query(10, ge=1, le=50, description="Number of messages to return"),
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get chat history.
    """
    try:
        history = await chat_service.get_history(conversation_id, limit)
        return {
            "success": True,
            "message": "History retrieved successfully",
            "count": len(history),
            "data": history
        }
    except Exception as e:
        logger.error(f"Error in get_history: {str(e)}")
        raise AppException(
            message=f"Failed to get history: {str(e)}",
            status_code=500,
            error_code="HISTORY_RETRIEVAL_FAILED"
        )


@router.delete(
    "/history",
    status_code=status.HTTP_200_OK,
    summary="Clear chat history",
    description="Clear conversation history"
)
async def clear_history(
    conversation_id: str = Query(..., description="Conversation ID"),
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Clear chat history.
    """
    try:
        result = await chat_service.clear_history(conversation_id)
        return {
            "success": True,
            "message": "History cleared successfully" if result else "Failed to clear history",
            "data": {"cleared": result}
        }
    except Exception as e:
        logger.error(f"Error in clear_history: {str(e)}")
        raise AppException(
            message=f"Failed to clear history: {str(e)}",
            status_code=500,
            error_code="HISTORY_CLEAR_FAILED"
        )


@router.get(
    "/reports/daily",
    status_code=status.HTTP_200_OK,
    summary="Generate daily report",
    description="Generate daily business report"
)
async def get_daily_report(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Generate daily business report.
    """
    try:
        report = await chat_service.generate_daily_report()
        return {
            "success": True,
            "message": "Daily report generated successfully",
            "data": report
        }
    except Exception as e:
        logger.error(f"Error in get_daily_report: {str(e)}")
        raise AppException(
            message=f"Failed to generate daily report: {str(e)}",
            status_code=500,
            error_code="REPORT_GENERATION_FAILED"
        )


@router.get(
    "/reports/weekly",
    status_code=status.HTTP_200_OK,
    summary="Generate weekly report",
    description="Generate weekly business report"
)
async def get_weekly_report(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Generate weekly business report.
    """
    try:
        report = await chat_service.generate_weekly_report()
        return {
            "success": True,
            "message": "Weekly report generated successfully",
            "data": report
        }
    except Exception as e:
        logger.error(f"Error in get_weekly_report: {str(e)}")
        raise AppException(
            message=f"Failed to generate weekly report: {str(e)}",
            status_code=500,
            error_code="REPORT_GENERATION_FAILED"
        )


@router.get(
    "/reports/monthly",
    status_code=status.HTTP_200_OK,
    summary="Generate monthly report",
    description="Generate monthly business report"
)
async def get_monthly_report(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Generate monthly business report.
    """
    try:
        report = await chat_service.generate_monthly_report()
        return {
            "success": True,
            "message": "Monthly report generated successfully",
            "data": report
        }
    except Exception as e:
        logger.error(f"Error in get_monthly_report: {str(e)}")
        raise AppException(
            message=f"Failed to generate monthly report: {str(e)}",
            status_code=500,
            error_code="REPORT_GENERATION_FAILED"
        )


@router.get(
    "/reports/quarterly",
    status_code=status.HTTP_200_OK,
    summary="Generate quarterly report",
    description="Generate quarterly business report"
)
async def get_quarterly_report(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Generate quarterly business report.
    """
    try:
        report = await chat_service.generate_quarterly_report()
        return {
            "success": True,
            "message": "Quarterly report generated successfully",
            "data": report
        }
    except Exception as e:
        logger.error(f"Error in get_quarterly_report: {str(e)}")
        raise AppException(
            message=f"Failed to generate quarterly report: {str(e)}",
            status_code=500,
            error_code="REPORT_GENERATION_FAILED"
        )


@router.get(
    "/reports/yearly",
    status_code=status.HTTP_200_OK,
    summary="Generate yearly report",
    description="Generate yearly business report"
)
async def get_yearly_report(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Generate yearly business report.
    """
    try:
        report = await chat_service.generate_yearly_report()
        return {
            "success": True,
            "message": "Yearly report generated successfully",
            "data": report
        }
    except Exception as e:
        logger.error(f"Error in get_yearly_report: {str(e)}")
        raise AppException(
            message=f"Failed to generate yearly report: {str(e)}",
            status_code=500,
            error_code="REPORT_GENERATION_FAILED"
        )


@router.get(
    "/reports/executive",
    status_code=status.HTTP_200_OK,
    summary="Generate executive summary",
    description="Generate one-click executive summary"
)
async def get_executive_summary(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Generate executive summary.
    """
    try:
        summary = await chat_service.generate_executive_summary()
        return {
            "success": True,
            "message": "Executive summary generated successfully",
            "data": summary
        }
    except Exception as e:
        logger.error(f"Error in get_executive_summary: {str(e)}")
        raise AppException(
            message=f"Failed to generate executive summary: {str(e)}",
            status_code=500,
            error_code="EXECUTIVE_SUMMARY_FAILED"
        )


@router.get(
    "/alerts",
    status_code=status.HTTP_200_OK,
    summary="Get business alerts",
    description="Get automatically generated business alerts"
)
async def get_alerts(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get business alerts.
    """
    try:
        alerts = await chat_service.get_business_alerts()
        return {
            "success": True,
            "message": "Business alerts retrieved successfully",
            "data": alerts
        }
    except Exception as e:
        logger.error(f"Error in get_alerts: {str(e)}")
        raise AppException(
            message=f"Failed to get business alerts: {str(e)}",
            status_code=500,
            error_code="ALERTS_GENERATION_FAILED"
        )


@router.get(
    "/action-plan",
    status_code=status.HTTP_200_OK,
    summary="Get action plan",
    description="Get prioritized business action plan"
)
async def get_action_plan(
    current_user: UserResponse = Depends(get_current_active_user)
) -> dict:
    """
    Get prioritized action plan.
    """
    try:
        action_plan = await chat_service.get_action_plan()
        return {
            "success": True,
            "message": "Action plan generated successfully",
            "data": action_plan
        }
    except Exception as e:
        logger.error(f"Error in get_action_plan: {str(e)}")
        raise AppException(
            message=f"Failed to get action plan: {str(e)}",
            status_code=500,
            error_code="ACTION_PLAN_FAILED"
        )