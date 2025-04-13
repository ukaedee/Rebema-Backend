from sqlalchemy.orm import Session
from models.user import User
from typing import Tuple, Dict, Any

def add_experience(user: User, xp: int, db: Session) -> Dict[str, Any]:
    """
    ユーザーに経験値を追加し、レベルアップの処理を行う

    Args:
        user (User): 経験値を追加するユーザー
        xp (int): 追加する経験値
        db (Session): データベースセッション

    Returns:
        Dict[str, Any]: 
            - leveled_up (bool): レベルアップしたかどうか
            - before_level (int): 追加前のレベル
            - before_xp (int): 追加前の経験値
            - after_level (int): 追加後のレベル
            - after_xp (int): 追加後の経験値
            - required_xp (int): 次のレベルに必要な経験値

    Note:
        - current_xpに経験値を加算
        - pointsに経験値を加算
        - レベルアップに必要な経験値に達した場合、レベルアップ処理を実行
        - レベルアップ後の必要経験値は 100
        - レベルアップした場合、experience_pointsに満たしたrequired_expを追加
    """
    # 経験値追加前のレベルと経験値を記録
    before_level = user.level
    before_xp = user.current_xp
    
    user.current_xp += xp
    required_xp = 100
    
    leveled_up = False
    earned_required_xp = 0
    
    while user.current_xp >= required_xp:
        user.current_xp -= required_xp
        user.level += 1
        leveled_up = True
        earned_required_xp += required_xp
    
    if leveled_up:
        user.experience_points += earned_required_xp
    
    db.commit()
    
    return {
        "level_up": leveled_up,
        "before_level": before_level,
        "before_xp": before_xp,
        "after_level": user.level,
        "after_xp": user.current_xp,
        "required_xp": required_xp
    }