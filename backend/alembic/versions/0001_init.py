from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('password_hash', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_table('workspaces',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_table('memberships',
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('workspace_id', sa.Integer, primary_key=True),
        sa.Column('role', sa.String, nullable=False)
    )
    op.create_table('documents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('workspace_id', sa.Integer, nullable=False),
        sa.Column('source', sa.String, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_table('chunks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('document_id', sa.Integer, nullable=False),
        sa.Column('chunk_index', sa.Integer, nullable=False),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('metadata_json', sa.JSON, nullable=True)
    )
    op.create_table('embeddings',
        sa.Column('chunk_id', sa.Integer, primary_key=True),
        sa.Column('embedding', Vector(384)),
        sa.Column('model_name', sa.String, nullable=False)
    )
    op.create_table('conversations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('workspace_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_table('messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('conversation_id', sa.Integer, nullable=False),
        sa.Column('role', sa.String, nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_table('approvals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('workspace_id', sa.Integer, nullable=False),
        sa.Column('requested_by', sa.Integer, nullable=False),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('proposed_tool_calls_json', sa.JSON, nullable=False),
        sa.Column('edited_tool_calls_json', sa.JSON, nullable=True),
        sa.Column('decision_by', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('decided_at', sa.DateTime, nullable=True)
    )
    op.create_table('tool_runs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('approval_id', sa.Integer, nullable=False),
        sa.Column('tool_name', sa.String, nullable=False),
        sa.Column('input_json', sa.JSON, nullable=False),
        sa.Column('output_json', sa.JSON, nullable=True),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('workspace_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=True),
        sa.Column('event_type', sa.String, nullable=False),
        sa.Column('payload_json', sa.JSON, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )
    op.create_table('eval_runs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('workspace_id', sa.Integer, nullable=False),
        sa.Column('metrics_json', sa.JSON, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('eval_runs')
    op.drop_table('audit_logs')
    op.drop_table('tool_runs')
    op.drop_table('approvals')
    op.drop_table('messages')
    op.drop_table('conversations')
    op.drop_table('embeddings')
    op.drop_table('chunks')
    op.drop_table('documents')
    op.drop_table('memberships')
    op.drop_table('workspaces')
    op.drop_table('users')
