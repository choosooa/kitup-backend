from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q, Value
from django.db.models.lookups import Exact

from core.choices import (
    IngredientUnit,
    RecommendationStatus,
    ReviewAnalysisStatus,
    TestStatus,
)
from core.models import TimeStampedModel


class MenuTest(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, db_column="test_id")
    menu_name = models.CharField(max_length=30, null=True, blank=True)
    selling_price = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )
    packaging_cost = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=Decimal("1000"),
        db_default=Decimal("1000"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    business_start_time = models.TimeField(null=True, blank=True)
    business_end_time = models.TimeField(null=True, blank=True)
    total_ingredient_cost = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("1"))],
    )
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    monthly_fixed_cost = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)]
    )
    improvement_result = models.JSONField(null=True, blank=True)
    review_analysis_status = models.CharField(
        max_length=20,
        choices=ReviewAnalysisStatus.choices,
        default=ReviewAnalysisStatus.PENDING,
        db_default=ReviewAnalysisStatus.PENDING,
    )
    improvement_status = models.CharField(
        max_length=20,
        choices=RecommendationStatus.choices,
        default=RecommendationStatus.PENDING,
        db_default=RecommendationStatus.PENDING,
    )

    class Meta:
        db_table = "tests"
        constraints = [
            models.CheckConstraint(
                condition=Q(menu_name__isnull=True) | Q(menu_name__regex=r"\S"),
                name="tests_menu_name_nonblank",
            ),
            models.CheckConstraint(
                condition=Q(selling_price__gte=1), name="tests_selling_price_min"
            ),
            models.CheckConstraint(
                condition=Q(packaging_cost__gte=0), name="tests_packaging_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(business_start_time__lt=F("business_end_time")),
                name="tests_business_time_order",
            ),
            models.CheckConstraint(
                condition=Q(total_ingredient_cost__gte=1),
                name="tests_ingredient_cost_min",
            ),
            models.CheckConstraint(
                condition=Q(ended_at__isnull=True)
                | (Q(started_at__isnull=False) & Q(ended_at__gt=F("started_at"))),
                name="tests_operating_time_order",
            ),
            models.CheckConstraint(
                condition=Q(monthly_fixed_cost__gte=0), name="tests_fixed_cost_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(review_analysis_status__in=ReviewAnalysisStatus.values),
                name="tests_review_analysis_status",
            ),
            models.CheckConstraint(
                condition=Q(improvement_status__in=RecommendationStatus.values),
                name="tests_improvement_status",
            ),
            # 생성 성공 시 JSON 객체 필수.
            models.CheckConstraint(
                condition=~Q(improvement_status=RecommendationStatus.SUCCEEDED)
                | (
                    Q(improvement_result__isnull=False)
                    & Exact(
                        models.Func(
                            F("improvement_result"),
                            function="jsonb_typeof",
                            output_field=models.CharField(),
                        ),
                        Value("object"),
                    )
                ),
                name="tests_succeeded_result_object",
            ),
        ]

    @property
    def status(self) -> TestStatus:
        if self.ended_at is not None:
            return TestStatus.COMPLETED
        if self.started_at is not None:
            return TestStatus.RUNNING
        return TestStatus.DRAFT


class Ingredient(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, db_column="ingredient_id")
    test = models.ForeignKey(MenuTest, on_delete=models.CASCADE, related_name="ingredients")
    ingredient_name = models.CharField(max_length=20)
    quantity = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0.0001"))],
    )
    unit = models.CharField(max_length=10, choices=IngredientUnit.choices)
    ingredient_cost = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0"))],
        db_comment="구매 단가",
    )

    class Meta:
        db_table = "ingredients"
        constraints = [
            models.UniqueConstraint(
                fields=["test", "ingredient_name"], name="ingredients_test_name_unique"
            ),
            models.CheckConstraint(
                condition=Q(ingredient_name__regex=r"\S"),
                name="ingredients_name_nonblank",
            ),
            models.CheckConstraint(
                condition=Q(quantity__gt=0), name="ingredients_quantity_positive"
            ),
            models.CheckConstraint(
                condition=Q(ingredient_cost__gte=0), name="ingredients_cost_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(unit__in=IngredientUnit.values), name="ingredients_unit_valid"
            ),
        ]
