"""Message: "${message}".

- Revision ID: ${up_revision}
- Previous: ${down_revision if down_revision else "None"| comma,n}
- Create Date: ${create_date}
"""

${imports if imports else ""}
## omit unused imports if migration contains no operations
% if upgrades or downgrades:
from alembic import op
import sqlalchemy as sa
% endif

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    % if upgrades:
        ${upgrades}
    % else:
        # Fill in upgrade operations, i.e.:
        # alembic.op.create_table("my_table", sqlalchemy.Column("id", sqlalchemy.Integer()))
        pass
    % endif


def downgrade() -> None:
    % if downgrades:
        ${downgrades}
    % else:
        # Fill in downgrade operations, i.e.:
        # alembic.op.drop_table("my_table")
        pass
    % endif
