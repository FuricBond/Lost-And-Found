"""
Notification service for in-app notifications.
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification, NotificationType
from app.models.user import User
from app.models.match import Match


class NotificationService:
    """
    Service for creating in-app notifications.
    """
    
    async def create_notification(
        self,
        db: AsyncSession,
        user_id: str,
        notification_type: NotificationType,
        subject: str,
        body: str,
        related_item_id: Optional[str] = None,
        related_match_id: Optional[str] = None
    ) -> Notification:
        """
        Create and store a notification record.
        
        Args:
            db: Database session
            user_id: Recipient user ID
            notification_type: Type of notification
            subject: Notification subject
            body: Notification body
            related_item_id: Optional related item
            related_match_id: Optional related match
        
        Returns:
            Created Notification object
        """
        notification = Notification(
            user_id=user_id,
            notification_type=notification_type.value,
            subject=subject,
            body=body,
            related_item_id=related_item_id,
            related_match_id=related_match_id,
            is_sent=True  # In-app notifications are always "sent"
        )
        
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        
        return notification
    
    async def notify_match_found(
        self,
        db: AsyncSession,
        user: User,
        match: Match,
        item_title: str
    ) -> Notification:
        """
        Send notification when a potential match is found.
        
        Args:
            db: Database session
            user: User to notify
            match: The match that was found
            item_title: Title of the matched item
        
        Returns:
            Created Notification
        """
        subject = f"Potential match found for your item!"
        body = f"""
Hello {user.full_name or 'there'},

We found a potential match for your item: {item_title}

Match Score: {match.overall_score:.0%}
Distance: {match.distance_km:.1f} km away

Please log in to review this match and confirm if it's your item.

Best regards,
Lost & Found Team
        """.strip()
        
        return await self.create_notification(
            db=db,
            user_id=user.id,
            notification_type=NotificationType.MATCH_FOUND,
            subject=subject,
            body=body,
            related_match_id=match.id
        )
    
    async def notify_match_confirmed(
        self,
        db: AsyncSession,
        user: User,
        match: Match,
        confirmer_name: str
    ) -> Notification:
        """
        Send notification when the other party confirms a match.
        
        Args:
            db: Database session
            user: User to notify
            match: The confirmed match
            confirmer_name: Name of the person who confirmed
        
        Returns:
            Created Notification
        """
        subject = "Match confirmed! Awaiting your confirmation"
        body = f"""
Hello {user.full_name or 'there'},

Great news! {confirmer_name} has confirmed the match.

Please log in to confirm from your side. Once both parties confirm,
you'll be able to see each other's contact information.

Best regards,
Lost & Found Team
        """.strip()
        
        return await self.create_notification(
            db=db,
            user_id=user.id,
            notification_type=NotificationType.MATCH_CONFIRMED,
            subject=subject,
            body=body,
            related_match_id=match.id
        )
    
    async def notify_contact_revealed(
        self,
        db: AsyncSession,
        user: User,
        other_user: User,
        match: Match
    ) -> Notification:
        """
        Send notification when both parties confirm and contact is revealed.
        
        Args:
            db: Database session
            user: User to notify
            other_user: The other party
            match: The confirmed match
        
        Returns:
            Created Notification
        """
        subject = "Contact information revealed!"
        body = f"""
Hello {user.full_name or 'there'},

Both parties have confirmed the match! Here is the contact information:

Name: {other_user.full_name or 'Not provided'}
Email: {other_user.email}
Phone: {other_user.phone_number or 'Not provided'}

Please reach out to coordinate the return of the item.

Best regards,
Lost & Found Team
        """.strip()
        
        return await self.create_notification(
            db=db,
            user_id=user.id,
            notification_type=NotificationType.CONTACT_REVEALED,
            subject=subject,
            body=body,
            related_match_id=match.id
        )


# Singleton instance
notification_service = NotificationService()
