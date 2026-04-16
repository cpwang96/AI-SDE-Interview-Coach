from fastapi import APIRouter, HTTPException

from models.schemas import AssessmentSubmission
from services.assessment import (
    start_assessment,
    get_assessment,
    evaluate_submission,
    save_assessment,
    generate_study_plan,
)
from services.question_bank import get_question
from services.user_service import get_profile

router = APIRouter()


@router.post("/start")
def begin_assessment(user_id: str):
    profile = get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found. Create a profile first.")
    result = start_assessment(user_id)
    # Return the first unanswered problem
    for p in result.problems:
        if not p.completed:
            question = get_question(question_id=p.question_id)
            return {
                "assessment_id": user_id,
                "current_problem": p.model_dump(),
                "question": question.model_dump(),
                "total_problems": len(result.problems),
                "completed_count": sum(1 for x in result.problems if x.completed),
            }
    return {"message": "Assessment already completed", "results": result.model_dump()}


@router.post("/submit")
def submit_answer(submission: AssessmentSubmission):
    result = get_assessment(submission.user_id)
    if not result:
        raise HTTPException(status_code=404, detail="No assessment found. Start one first.")

    # Find the problem
    problem = None
    for p in result.problems:
        if p.question_id == submission.question_id:
            problem = p
            break

    if not problem:
        raise HTTPException(status_code=400, detail="Question not in assessment")

    # Get question title for evaluation context
    question = get_question(question_id=submission.question_id)

    # Evaluate with Claude
    eval_result = evaluate_submission(submission, question.title)
    problem.completed = True
    problem.user_code = submission.code
    problem.score = eval_result["score"]
    problem.coach_evaluation = eval_result["evaluation"]

    # Update topic scores
    result.topic_scores[problem.topic] = eval_result["score"]

    # Check if assessment is complete
    all_done = all(p.completed for p in result.problems)
    if all_done:
        avg = sum(p.score or 0 for p in result.problems) / len(result.problems)
        if avg >= 80:
            result.overall_level = "advanced"
        elif avg >= 50:
            result.overall_level = "intermediate"
        else:
            result.overall_level = "beginner"

    save_assessment(result)

    # Return next problem or final results
    response = {
        "evaluation": eval_result,
        "completed_count": sum(1 for p in result.problems if p.completed),
        "total_problems": len(result.problems),
    }

    if all_done:
        # Generate study plan
        profile = get_profile(submission.user_id)
        background = ""
        if profile:
            background = f"Name: {profile.name}, Target: {profile.target_role}, Experience: {profile.years_of_experience} years"
            if profile.resume_text:
                background += f"\nResume: {profile.resume_text[:500]}"

        study_plan = generate_study_plan(submission.user_id, background)
        result.study_plan = study_plan
        save_assessment(result)

        response["assessment_complete"] = True
        response["overall_level"] = result.overall_level
        response["study_plan"] = study_plan
    else:
        # Return next problem
        for p in result.problems:
            if not p.completed:
                question = get_question(question_id=p.question_id)
                response["next_problem"] = p.model_dump()
                response["next_question"] = question.model_dump()
                break

    return response


@router.get("/results/{user_id}")
def get_results(user_id: str):
    result = get_assessment(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="No assessment found")
    return result.model_dump()
